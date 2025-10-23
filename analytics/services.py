# analytics/services.py
from analytics.models import AssocRule, CustomerCluster

def recommend_from_cart(cart_skus, top_n=5, min_conf=0.1, min_lift=1.05):
    cart = set(map(str, cart_skus))
    qs = (AssocRule.objects
          .filter(confidence__gte=min_conf, lift__gte=min_lift)
          .order_by("-lift","-confidence","-support"))
    scored = {}
    for r in qs.iterator():
        ants = set(r.antecedents)
        if ants.issubset(cart):
            for c in r.consequents:
                if c not in cart:
                    cur = scored.get(c)
                    met = (r.lift, r.confidence, r.support)
                    if not cur or met > cur:
                        scored[c] = met
    return [sku for sku, _ in sorted(scored.items(), key=lambda kv: kv[1], reverse=True)[:top_n]]

def customer_cluster_id(user):
    rec = CustomerCluster.objects.filter(customer=user).order_by("-fitted_at").first()
    return rec.cluster_id if rec else None
