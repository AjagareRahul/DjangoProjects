from django.contrib import admin
from .models import Material, Cart, CartItem, Order, OrderItem

class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'image']

admin.site.register(Material, MaterialAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'created_at']
    list_editable = ['status']

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
