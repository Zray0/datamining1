# carts/views.py (example usage)
from analytics.services import recommend_from_cart

def cart_view(request):
    cart_skus = [li.product.sku for li in request.cart.items.all()]
    recs = recommend_from_cart(cart_skus, top_n=5, min_conf=0.1, min_lift=1.05)
    # join to product names/prices for display
    from inventory.models import Product
    rec_products = list(Product.objects.filter(sku__in=recs))
    return render(request, "cart.html", {"recommendations": rec_products})
