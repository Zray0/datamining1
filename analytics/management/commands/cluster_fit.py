from django.core.management.base import BaseCommand
from django.db import transaction
from analytics.models import CustomerCluster, ProductCluster
import pandas as pd

class Command(BaseCommand):
    help = "Fit KMeans clusters for customers and products"

    def add_arguments(self, p):
        p.add_argument("--entity", choices=["customers","products","both"], default="both")
        p.add_argument("--k_min", type=int, default=2)
        p.add_argument("--k_max", type=int, default=6)
        p.add_argument("--csv_customers", type=str, default="")
        p.add_argument("--csv_products", type=str, default="")

    def _load_customer_features(self, path):
        # expected columns:
        # customer_id,total_spent,purchase_freq,pct_protein,pct_vitamins,pct_accessories,preferred_channel
        return pd.read_csv(path) if path else pd.DataFrame()

    def _load_product_features(self, path):
        # expected columns:
        # sku,monthly_sales,shelf_life_days,profit_margin,category
        return pd.read_csv(path) if path else pd.DataFrame()

    def _cluster(self, df, num_cols, cat_cols, k_min, k_max):
        if df.empty: return None, None
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import StandardScaler, OneHotEncoder
        from sklearn.pipeline import Pipeline
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
        X = df[num_cols + cat_cols]
        prep = ColumnTransformer([
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ])
        best_score, best_k, best_labels = -1, None, None
        for k in range(k_min, k_max+1):
            pipe = Pipeline([("prep", prep), ("km", KMeans(n_clusters=k, n_init="auto", random_state=42))])
            Xt = pipe.named_steps["prep"].fit_transform(X)
            labels = pipe.named_steps["km"].fit_predict(Xt)
            try:
                score = silhouette_score(Xt, labels)
            except Exception:
                score = -1
            if score > best_score:
                best_score, best_k, best_labels = score, k, labels
        return best_labels, best_k

    def handle(self, *a, **o):
        # Customers
        if o["entity"] in ("customers","both"):
            dfc = self._load_customer_features(o["csv_customers"])
            if not dfc.empty:
                num = ["total_spent","purchase_freq","pct_protein","pct_vitamins","pct_accessories"]
                cat = ["preferred_channel"]
                labels, k = self._cluster(dfc, num, cat, o["k_min"], o["k_max"])
                if labels is not None:
                    with transaction.atomic():
                        CustomerCluster.objects.all().delete()
                        CustomerCluster.objects.bulk_create([
                            CustomerCluster(
                                customer=None,
                                customer_key=str(c),
                                cluster_id=int(lbl),
                                algo="kmeans",
                                k=k,
                                features={}
                            )
                            for c, lbl in zip(dfc["customer_id"].tolist(), labels)
                        ], batch_size=2000)
                    self.stdout.write(self.style.SUCCESS(f"Customer clusters saved (k={k})"))
            else:
                self.stdout.write(self.style.WARNING("No customer features"))

        # Products
        if o["entity"] in ("products","both"):
            dfp = self._load_product_features(o["csv_products"])
            if not dfp.empty:
                num = ["monthly_sales","shelf_life_days","profit_margin"]
                cat = ["category"]
                labels, k = self._cluster(dfp, num, cat, o["k_min"], o["k_max"])
                if labels is not None:
                    with transaction.atomic():
                        ProductCluster.objects.all().delete()
                        ProductCluster.objects.bulk_create([
                            ProductCluster(
                                sku=str(s),
                                cluster_id=int(lbl),
                                algo="kmeans",
                                k=k,
                                features={}
                            )
                            for s, lbl in zip(dfp["sku"].tolist(), labels)
                        ], batch_size=2000)
                    self.stdout.write(self.style.SUCCESS(f"Product clusters saved (k={k})"))
            else:
                self.stdout.write(self.style.WARNING("No product features"))
