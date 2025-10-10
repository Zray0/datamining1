from django.shortcuts import render
from django.db.models import Sum, Avg
from inventory.models import SupplementData

def dashboard_home(request):
    total_revenue = SupplementData.objects.aggregate(total=Sum('revenue'))['total'] or 0
    total_orders = SupplementData.objects.aggregate(total=Sum('units_sold'))['total'] or 0

    top_product = SupplementData.objects.order_by('-units_sold').first()
    top_product_name = top_product.product_name if top_product else '-'

    low_stock = SupplementData.objects.filter(units_returned__gt=0).count()
    avg_satisfaction = SupplementData.objects.aggregate(avg=Avg('satisfaction'))['avg'] or 0

    sales_data = SupplementData.objects.order_by('-date')[:10][::-1]
    chart_labels = [s.date.strftime("%b %d") for s in sales_data]
    chart_data = [float(s.revenue) for s in sales_data]

    category_data = (
        SupplementData.objects
        .values('category')
        .annotate(total_revenue=Sum('revenue'))
        .order_by('-total_revenue')[:5]
    )
    inv_labels = [c['category'] for c in category_data]
    inv_data = [float(c['total_revenue']) for c in category_data]

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'top_product': top_product_name,
        'low_stock': low_stock,
        'avg_satisfaction': round(avg_satisfaction, 2),
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'inv_labels': inv_labels,
        'inv_data': inv_data,
    }

    return render(request, 'dashboards/dashboard_home.html', context)
