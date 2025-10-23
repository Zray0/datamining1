# analytics/management/commands/mine_rules.py
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from analytics.models import AssocRule
import pandas as pd, os

class Command(BaseCommand):
    help = "Mine frequent itemsets and association rules from sales or CSV"
    def add_arguments(self, p):
        p.add_argument("--min_support", type=float, default=0.01)
        p.add_argument("--min_conf", type=float, default=0.30)
        p.add_argument("--min_lift", type=float, default=1.05)
        p.add_argument("--sku_field", type=str, default="sku")
        p.add_argument("--csv_path", type=str, default="mba_required_transactions.csv")
        p.add_argument("--max_rules", type=int, default=5000)

    def _baskets_from_db(self, sku_field):
        try:
            from sales.models import OrderItem
        except Exception:
            return []
        expr = f"product__{sku_field}"
        try:
            qs = (OrderItem.objects.select_related("order","product")
                  .order_by("order_id").values_list("order_id", expr))
            _ = qs[:1]
        except Exception:
            qs = (OrderItem.objects.select_related("order","product")
                  .order_by("order_id").values_list("order_id","product_id"))
        baskets = {}
        for oid, key in qs:
            if key is None: continue
            baskets.setdefault(oid, set()).add(str(key))
        return [sorted(list(s)) for s in baskets.values() if s]

    def _baskets_from_csv(self, path):
        if not os.path.exists(path): return []
        df = pd.read_csv(path, dtype={"transaction_id": str, "item_id": str})
        if df.empty or "transaction_id" not in df or "item_id" not in df: return []
        grp = df.groupby("transaction_id")["item_id"].apply(lambda s: sorted(set(s)))
        return grp.tolist()

    def _mine(self, dataset, s, c, l):
        from mlxtend.preprocessing import TransactionEncoder
        from mlxtend.frequent_patterns import fpgrowth, association_rules
        te = TransactionEncoder()
        df = pd.DataFrame(te.fit(dataset).transform(dataset), columns=te.columns_)
        itemsets = fpgrowth(df, min_support=s, use_colnames=True)
        if itemsets.empty: return pd.DataFrame()
        rules = association_rules(itemsets, metric="confidence", min_threshold=c)
        if rules.empty: return pd.DataFrame()
        return rules[rules["lift"] >= l]

    def handle(self, *a, **o):
        dataset = self._baskets_from_db(o["sku_field"]) or self._baskets_from_csv(o["csv_path"])
        if not dataset: raise CommandError("No transactions found to mine (dataset is empty)")
        try:
            import mlxtend  # noqa
        except Exception as ex:
            raise CommandError(f"mlxtend is required (pip install mlxtend): {ex}")
        s_grid = [o["min_support"], o["min_support"]/2, 0.005, 0.002, 0.001]
        c_grid = [o["min_conf"], 0.2, 0.1]
        l_grid = [o["min_lift"], 1.0]
        import pandas as pd
        rules = pd.DataFrame()
        for s in s_grid:
            for c in c_grid:
                for l in l_grid:
                    rules = self._mine(dataset, s, c, l)
                    if not rules.empty:
                        self.stdout.write(self.style.SUCCESS(f"Found {len(rules)} rules at support={s}, conf={c}, lift={l}"))
                        break
                if not rules.empty: break
            if not rules.empty: break
        if rules.empty:
            self.stdout.write(self.style.WARNING("No rules after search"))
            return
        rules = rules.sort_values(["lift","confidence","support"], ascending=False).head(int(o["max_rules"]))
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
