
# analytics/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import AssocRule


# analytics/views.py (add)
from django.shortcuts import render

def rules_page(request):
    rules = (AssocRule.objects
             .order_by("-lift","-confidence","-support")[:200])
    return render(request, "analytics/rules.html", {"rules": rules})


@require_GET
def rules_api(request):
    min_conf = float(request.GET.get("min_conf", 0.1))
    min_lift = float(request.GET.get("min_lift", 1.0))
    limit = int(request.GET.get("limit", 100))
    qs = (AssocRule.objects
          .filter(confidence__gte=min_conf, lift__gte=min_lift)
          .order_by("-lift","-confidence","-support")[:limit])
    data = [{
        "antecedents": r.antecedents,
        "consequents": r.consequents,
        "support": r.support,
        "confidence": r.confidence,
        "lift": r.lift,
    } for r in qs]
    return JsonResponse({"rules": data})
