from django.contrib import admin

try:
    from .models import AssocRule, CustomerCluster, ProductCluster
except Exception:
    AssocRule = CustomerCluster = ProductCluster = None

if AssocRule:
    @admin.register(AssocRule)
    class AssocRuleAdmin(admin.ModelAdmin):
        list_display = ("show_antecedents","show_consequents","support","confidence","lift")
        ordering = ("-lift","-confidence","-support")
        def show_antecedents(self, obj): return ", ".join(obj.antecedents or [])
        def show_consequents(self, obj): return ", ".join(obj.consequents or [])

if CustomerCluster:
    @admin.register(CustomerCluster)
    class CustomerClusterAdmin(admin.ModelAdmin):
        list_display = ("customer_key","customer","cluster_id","k","algo","fitted_at")
        search_fields = ("customer_key","customer__username","customer__email")
        list_filter = ("cluster_id","k","algo")

if ProductCluster:
    @admin.register(ProductCluster)
    class ProductClusterAdmin(admin.ModelAdmin):
        list_display = ("sku","cluster_id","k","algo","fitted_at")
        search_fields = ("sku",)
        list_filter = ("cluster_id","k","algo")
