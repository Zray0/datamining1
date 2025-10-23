from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from sales.models import Order, OrderItem
from inventory.models import Product
from analytics.models import AssocRule, CustomerCluster
from inventory.models import Product

@login_required
def dashboard(request):
    user = request.user
    products = Product.objects.all()
    orders = Order.objects.filter(user=user).order_by('-created_at')
    context = {
        'user': user,
        'products': products,
        'orders': orders,
        'cluster_name': cluster_name,
        # ...other context
    }
    # Get cluster info
    try:
        cluster = user.customer_cluster
        cluster_name = cluster.cluster_name
    except CustomerCluster.DoesNotExist:
        cluster_name = None

    # Product list for ordering
    products = Product.objects.all()

    # Purchase/order stats
    orders = Order.objects.filter(user=user).order_by('-created_at')
    order_items = OrderItem.objects.filter(order__user=user).select_related('product')
    total_orders = orders.count()
    total_spent = orders.aggregate(total=Sum('total_amount'))['total'] or 0

    context = {
        "cluster_name": cluster_name,
        "products": products,
        "orders": orders,
        "total_orders": total_orders,
        "total_spent": total_spent,
    }
    return render(request, "customer/dashboard.html", context)

from cart.models import Cart, CartItem
from inventory.models import Product

@login_required
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        return redirect("cart_view")
    else:
        return redirect("dashboard")
