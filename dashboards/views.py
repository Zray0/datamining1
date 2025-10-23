# dashboards/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from analytics.services import recommend_from_cart, customer_cluster_id

@login_required
def dashboard_home(request):
    cid = customer_cluster_id(request.user)
    return render(request, "dashboards/dashboard_home.html", {"cluster_id": cid})
