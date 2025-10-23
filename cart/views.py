from django.contrib.auth.decorators import login_required

from analytics.models import AssocRule, CustomerCluster
from cart.models import CartItem, Cart

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_product_names = [item.product.name for item in cart_items]
    recommendations = AssocRule.objects.filter(antecedent__in=cart_product_names).order_by('-confidence')[:5]
    
    # Cluster info
    try:
        cluster = request.user.customer_cluster
        cluster_name = cluster.cluster_name
    except CustomerCluster.DoesNotExist:
        cluster_name = None

    context = {
        'cart_items': cart_items,
        'recommendations': recommendations,
        'cluster_name': cluster_name,
    }
    return render(request, "cart/cart.html", context)
