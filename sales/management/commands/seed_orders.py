# sales/management/commands/seed_orders.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from inventory.models import Product, Category
from sales.models import Order, OrderItem
import pandas as pd

User = get_user_model()

class Command(BaseCommand):
    help = "Seed example Orders/OrderItems from supplements_data.xlsx"

    def add_arguments(self, parser):
        parser.add_argument("--xlsx", default="supplements_data.xlsx")
        parser.add_argument("--limit", type=int, default=20)

    def handle(self, *args, **opts):
        df = pd.read_excel(opts["xlsx"])
        df.columns = [c.strip().replace("\n", " ").replace(" ", "_") for c in df.columns]
        needed = {"Date","Product_Name","Category","Units_Sold","Price","Platform","Location"}
        if not needed.issubset(set(df.columns)):
            self.stdout.write(self.style.WARNING("Dataset missing required columns"))
            return

        # ensure categories/products exist
        from django.utils.text import slugify
        for name, cat in df[["Product_Name","Category"]].drop_duplicates().values.tolist():
            cat_obj, _ = Category.objects.get_or_create(name=cat, defaults={"slug": slugify(cat)})
            Product.objects.get_or_create(
                sku=slugify(name).upper().replace("-", "_")[:40],
                defaults={"name": name, "category": cat_obj, "margin": 0.30},
            )

        # optional user
        user = User.objects.first()

        rows = df.head(opts["limit"]).to_dict("records")
        created = 0
        for r in rows:
            sku = (r["Product_Name"] or "").strip()
            from django.utils.text import slugify as s
            prod = Product.objects.filter(sku=s(sku).upper().replace("-", "_")[:40]).first()
            if not prod:
                continue
            order = Order.objects.create(
                created_at=timezone.now(),
                user=user,
                platform=str(r.get("Platform") or ""),
                location=str(r.get("Location") or ""),
            )
            qty = int(max(1, float(r.get("Units_Sold") or 1)))
            price = float(r.get("Price") or 0.0)
            OrderItem.objects.create(order=order, product=prod, quantity=qty, price=price)
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created} orders"))
