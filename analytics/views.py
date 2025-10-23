# analytics/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import AssocRule, CustomerCluster, ProductCluster

@staff_member_required
def rules_page(request):
    rules = AssocRule.objects.order_by("-lift","-confidence","-support")[:200]
    return render(request, "analytics/rules.html", {"rules": rules})

@staff_member_required
def clusters_overview(request):
    cust = CustomerCluster.objects.order_by("cluster_id","customer_id")[:200]
    prod = ProductCluster.objects.order_by("cluster_id","sku")[:200]
    return render(request, "analytics/clusters_overview.html", {"customer_clusters": cust, "product_clusters": prod})

from analytics.models import AssocRule, CustomerCluster, ProductCluster

def analytics_dashboard(request):
    # Top association rules, sorted by lift or confidence
    top_assoc = AssocRule.objects.order_by('-confidence')[:5]

    # Cluster summaries (e.g., number of customers per cluster)
    customer_clusters = (
        CustomerCluster.objects
        .values('cluster_id')
        .annotate(num_customers=Count('customer'))
        .order_by('-num_customers')
    )

    product_clusters = (
        ProductCluster.objects
        .values('cluster_id')
        .annotate(num_products=Count('product'))
        .order_by('-num_products')
    )

    return render(request, "analytics/analytics_dashboard.html", {
        "top_assoc": top_assoc,
        "customer_clusters": customer_clusters,
        "product_clusters": product_clusters,
    })
