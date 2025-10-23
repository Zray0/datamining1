from django.core.management.base import BaseCommand
from django.utils.text import slugify
from inventory.models import Category, Product
import csv

class Command(BaseCommand):
    help = "Seed categories and products from inventory_seed.csv"

    def add_arguments(self, parser):
        parser.add_argument("--csv_path", default="inventory_seed.csv")

    def handle(self, *args, **opts):
        path = opts["csv_path"]
        created_c = created_p = 0
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                cat, c_new = Category.objects.get_or_create(
                    name=row["category"],
                    defaults={"slug": row.get("slug") or slugify(row["category"])},
                )
                _, p_new = Product.objects.get_or_create(
                    sku=row["sku"],
                    defaults={"name": row["name"], "category": cat, "margin": 0.30},
                )
                created_c += int(c_new)
                created_p += int(p_new)
        self.stdout.write(self.style.SUCCESS(f"Categories new: {created_c}, Products new: {created_p}"))
