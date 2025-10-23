from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from inventory.models import Product
from .models import Order, OrderItem,DashboardStats
from django.shortcuts import redirect

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ("product",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "user", "platform", "location")
    list_filter = ("platform", "location", "created_at")
    search_fields = ("id", "user__username", "user__email", "platform", "location")
    list_select_related = ("user",)
    inlines = (OrderItemInline,)

    def changelist_view(self, request, extra_context=None):
        # Redirect to dashboard if query param present
        if 'dashboard' in request.GET:
            return HttpResponseRedirect('/sales/dashboard/')

        # Low stock alert for inventory products
        #low_stock = Product.objects.filter(stock__lt=10)
        #if low_stock.exists():
           # messages.warning(request, f"{low_stock.count()} products are low on stock!")

        return super().changelist_view(request, extra_context)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price")
    list_select_related = ("order", "product")
    search_fields = ("order__id", "product__sku", "product__name")



@admin.register(DashboardStats)
class DashboardStatsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
    def get_model_perms(self, request):  # Only show "change"
        return {'change': True}
    def changelist_view(self, request, extra_context=None):
        return redirect('/sales/dashboard/')
