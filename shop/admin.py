from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # 不自动额外生成空白行

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'status', 'total_amount', 'created_at')
    search_fields = ('order_number', 'customer_name')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
# Register your models here.
