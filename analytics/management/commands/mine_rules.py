# analytics/management/commands/mine_rules.py
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from analytics.models import AssocRule
import pandas as pd
import os

class Command(BaseCommand):
    help = "Mine frequent itemsets and association rules from sales tables or CSV; auto-tune thresholds and fallback to pairwise if needed"

    def add_arguments(self, parser):
        parser.add_argument("--min_support", type=float, default=0.01, help="Initial min support (e.g., 0.01)")
        parser.add_argument("--min_conf", type=float, default=0.30, help="Initial min confidence (e.g., 0.30)")
        parser.add_argument("--min_lift", type=float, default=1.05, help="Initial min lift (e.g., 1.05)")
        parser.add_argument("--sku_field", type=str, default="sku", help="Product field to use (default: sku; fallback to id)")
        parser.add_argument("--csv_path", type=str, default="mba_required_transactions.csv",
                            help="Fallback CSV with columns: transaction_id,item_id")
        parser.add_argument("--max_rules", type=int, default=5000, help="Cap number of saved rules")

    def _baskets_from_db(self, sku_field):
        try:
            from sales.models import OrderItem
        except Exception as ex:
            self.stdout.write(self.style.WARNING(f"DB source unavailable: {ex}"))
            return []
        key_expr = f"product__{sku_field}"
        try:
            qs = (OrderItem.objects
                  .select_related("order", "product")
                  .order_by("order_id")
                  .values_list("order_id", key_expr))
            _ = qs[:1]
        except Exception:
            qs = (OrderItem.objects
                  .select_related("order", "product")
                  .order_by("order_id")
                  .values_list("order_id", "product_id"))
        baskets = {}
        for oid, key in qs:
            if key is None:
                continue
            k = str(key)
            baskets.setdefault(oid, set()).add(k)
        dataset = [sorted(list(s)) for s in baskets.values() if s]
        return dataset

    def _baskets_from_csv(self, csv_path):
        if not os.path.exists(csv_path):
            return []
        df = pd.read_csv(csv_path, dtype={"transaction_id": str, "item_id": str})
        if df.empty or "transaction_id" not in df or "item_id" not in df:
            return []
        grp = df.groupby("transaction_id")["item_id"].apply(lambda s: sorted(set(s.astype(str))))
        return grp.tolist()

    def _mine_rules(self, dataset, min_support, min_conf, min_lift):
        from mlxtend.preprocessing import TransactionEncoder
        from mlxtend.frequent_patterns import fpgrowth, association_rules
        te = TransactionEncoder()
        df = pd.DataFrame(te.fit(dataset).transform(dataset), columns=te.columns_)
        itemsets = fpgrowth(df, min_support=min_support, use_colnames=True)
        if itemsets.empty:
            return pd.DataFrame()
        rules = association_rules(itemsets, metric="confidence", min_threshold=min_conf)
        if rules.empty:
            return pd.DataFrame()
        rules = rules[rules["lift"] >= min_lift]
        return rules

    def _pairwise_fallback(self, dataset, min_support=0.001, min_conf=0.05):
        # Simple pairwise counts to produce at least some rules when FP-Growth yields none
        from collections import Counter
        import itertools
        N = len(dataset)
        if N == 0:
            return pd.DataFrame()
        item_counts = Counter()
        pair_counts = Counter()
        for basket in dataset:
            uniq = set(basket)
            for i in uniq:
                item_counts[i] += 1
            for a, b in itertools.combinations(sorted(uniq), 2):
                pair_counts[(a, b)] += 1
        rows = []
        for (a, b), c_ab in pair_counts.items():
            supp = c_ab / N
            if supp < min_support:
                continue
            conf_ab = c_ab / item_counts[a] if item_counts[a] else 0.0
            conf_ba = c_ab / item_counts[b] if item_counts[b] else 0.0
            supp_a = item_counts[a] / N
            supp_b = item_counts[b] / N
            lift_ab = conf_ab / supp_b if supp_b else 0.0
            lift_ba = conf_ba / supp_a if supp_a else 0.0
            if conf_ab >= min_conf:
                rows.append({"antecedents": {a}, "consequents": {b}, "support": supp,
                             "confidence": conf_ab, "lift": lift_ab, "leverage": 0.0, "conviction": 0.0})
            if conf_ba >= min_conf:
                rows.append({"antecedents": {b}, "consequents": {a}, "support": supp,
                             "confidence": conf_ba, "lift": lift_ba, "leverage": 0.0, "conviction": 0.0})
        return pd.DataFrame(rows)

    def handle(self, *args, **opts):
        # 1) Build dataset from DB, else CSV
        dataset = self._baskets_from_db(opts["sku_field"])
        if not dataset:
            self.stdout.write(self.style.WARNING("DB returned no baskets; trying CSV fallback"))
            dataset = self._baskets_from_csv(opts["csv_path"])
        if not dataset:
            raise CommandError("No transactions found to mine (dataset is empty)")

        # 2) Try initial thresholds, else auto-tune
        try:
            from mlxtend.preprocessing import TransactionEncoder  # noqa: F401
            from mlxtend.frequent_patterns import fpgrowth, association_rules  # noqa: F401
        except Exception as ex:
            raise CommandError(f"mlxtend is required (pip install mlxtend): {ex}")

        init_sup = max(1e-4, float(opts["min_support"]))
        init_conf = max(0.01, float(opts["min_conf"]))
        init_lift = max(1.0, float(opts["min_lift"]))
        support_grid = [init_sup, init_sup/2, init_sup/5, init_sup/10, 0.001, 0.0005, 0.0001]
        conf_grid = [init_conf, 0.2, 0.1, 0.05]
        lift_grid = [init_lift, 1.0]

        rules = pd.DataFrame()
        for s in support_grid:
            for c in conf_grid:
                for l in lift_grid:
                    rules = self._mine_rules(dataset, s, c, l)
                    if not rules.empty:
                        self.stdout.write(self.style.SUCCESS(f"Found {len(rules)} rules at support={s}, conf={c}, lift={l}"))
                        break
                if not rules.empty:
                    break
            if not rules.empty:
                break

        # 3) Pairwise fallback if still empty
        if rules.empty:
            self.stdout.write(self.style.WARNING("FP-Growth produced no rules; generating pairwise fallback"))
            rules = self._pairwise_fallback(dataset, min_support=0.001, min_conf=0.05)
            if rules.empty:
                self.stdout.write(self.style.WARNING("Pairwise fallback produced no rules"))
                return

        # 4) Persist rules
        rules = rules.sort_values(["lift", "confidence", "support"], ascending=False).head(int(opts["max_rules"]))
        with transaction.atomic():
            AssocRule.objects.all().delete()
            AssocRule.objects.bulk_create([
                AssocRule(
                    antecedents=sorted(list(r["antecedents"])),
                    consequents=sorted(list(r["consequents"])),
                    support=float(r["support"]),
                    confidence=float(r["confidence"]),
                    lift=float(r["lift"]),
                    leverage=float(r.get("leverage", 0.0)),
                    conviction=float(r.get("conviction", 0.0)),
                ) for _, r in rules.iterrows()
            ], batch_size=2000)

        self.stdout.write(self.style.SUCCESS(f"Saved {len(rules)} rules to analytics.AssocRule"))
