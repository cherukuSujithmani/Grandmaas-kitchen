from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.contrib.admin import AdminSite
from django.db.models import Sum
from .models import Product, Order, OrderItem, Wishlist, Address

# Custom AdminSite
class MyAdminSite(AdminSite):
    site_header = "Grandma's Kitchen Admin"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view))
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        total_orders = Order.objects.count()
        total_revenue = sum(order.total_price for order in Order.objects.all())
        total_products = Product.objects.count()
        top_products = OrderItem.objects.values('product__name').annotate(
            total_sold=Sum('quantity')).order_by('-total_sold')[:5]

        context = dict(
            self.each_context(request),
            total_orders=total_orders,
            total_revenue=total_revenue,
            total_products=total_products,
            top_products=top_products,
        )
        return TemplateResponse(request, "admin/dashboard.html", context)

custom_admin_site = MyAdminSite(name='myadmin')

# --- Model Admins ---

# Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

    def is_available(self, obj):
        return obj.stock > 0
    is_available.boolean = True

# OrderItem Inline (optional if you want to add to OrderAdmin later)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# Order Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'status', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('status', 'created_at')
    actions = ['mark_as_shipped']

    @admin.action(description="Mark selected orders as Shipped")
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status='Shipped')
        self.message_user(request, f"{updated} order(s) marked as shipped.")

# OrderItem Admin
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'subtotal')
    search_fields = ('product__name', 'order__id')

    def subtotal(self, obj):
        return obj.quantity * obj.price

# Address Admin
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'street', 'city', 'postal_code', 'phone')
    search_fields = ('user__username', 'full_name', 'city', 'postal_code')

# Wishlist Admin
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    search_fields = ('user__username', 'product__name')

# --- Register All Models to the Custom Admin Site ---
custom_admin_site.register(Product, ProductAdmin)
custom_admin_site.register(Order, OrderAdmin)
custom_admin_site.register(OrderItem, OrderItemAdmin)
custom_admin_site.register(Address, AddressAdmin)
custom_admin_site.register(Wishlist, WishlistAdmin)
