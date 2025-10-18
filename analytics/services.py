# analytics/services.py
from analytics.models import AssocRule
def recommend_from_cart(cart_skus, top_n=5, min_conf=0.1, min_lift=1.05):
    cart = set(str(x) for x in cart_skus)
    qs = (AssocRule.objects
          .filter(confidence__gte=min_conf, lift__gte=min_lift)
          .order_by("-lift","-confidence","-support"))
    scored = {}
    for r in qs.iterator():
        ants = set(r.antecedents)
        if ants.issubset(cart):
            for c in r.consequents:
                if c not in cart:
                    m = scored.get(c)
                    cur = (r.lift, r.confidence, r.support)
                    if not m or cur > (m["lift"], m["confidence"], m["support"]):
                        scored[c] = {"lift": r.lift, "confidence": r.confidence, "support": r.support}
    return [sku for sku, _ in sorted(scored.items(), key=lambda kv: (kv[1]['lift'], kv[1]['confidence']), reverse=True)[:top_n]]
