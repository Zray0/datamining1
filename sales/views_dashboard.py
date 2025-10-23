from django.db.models import Sum, Count, Avg, F
from django.utils import timezone
from django.contrib.auth import get_user_model
from sales.models import Order, OrderItem
from inventory.models import Product
from django.shortcuts import render

def sales_dashboard(request):
    now = timezone.now()

    # 1. Sales/order stats
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    avg_order_value = Order.objects.aggregate(avg=Avg('total_amount'))['avg'] or 0

    # 2. Customers stats
    User = get_user_model()
    total_customers = User.objects.filter(orders__isnull=False).distinct().count()
    repeat_customers = (
        User.objects.annotate(order_count=Count('orders'))
        .filter(order_count__gt=1).count()
    )
    top_customers = (
        Order.objects.values('user__username')
        .annotate(spent=Sum('total_amount'))
        .order_by('-spent')[:5]
    )

    # 3. Sales Time series (monthly)
    monthly_sales = (
        Order.objects.filter(created_at__year=now.year)
        .values(month=F('created_at__month'))
        .annotate(revenue=Sum('total_amount'))
        .order_by('month')
    )

    # 4. Bestsellers
    bestsellers = (
        OrderItem.objects
        .values('product__name')
        .annotate(quantity_sold=Sum('quantity'))
        .order_by('-quantity_sold')[:5]
    )

    # 5. Low inventory (requires a quantity field on Product)
    if hasattr(Product, 'quantity'):
        low_inventory = (
            Product.objects.filter(quantity__lte=10)
            .order_by('quantity')[:5]
        )
    else:
        low_inventory = Product.objects.none()

    # 6. Admin users
    admin_members = User.objects.filter(is_staff=True).order_by('username')

    context = {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "avg_order_value": avg_order_value,
        "total_customers": total_customers,
        "repeat_customers": repeat_customers,
        "top_customers": top_customers,
        "monthly_sales": list(monthly_sales),
        "bestsellers": bestsellers,
        "low_inventory": low_inventory,
        "admin_members": admin_members,
    }
    return render(request, "sales/sales_dashboard.html", context)
