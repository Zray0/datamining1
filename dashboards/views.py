# dashboards/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

@login_required
def dashboard_home(request):
    return render(request, "dashboards/customer.html")

@staff_member_required
def admin_dashboard(request):
    return render(request, "dashboards/admin_dashboard.html")
