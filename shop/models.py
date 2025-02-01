from django.db import models

# Create your models here.
class Order(models.Model):
    ORDER_STATUS = [
        ('pending', '待处理'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    order_number = models.CharField(max_length=20, unique=True, verbose_name="订单号")
    customer_name = models.CharField(max_length=100, verbose_name="客户名称")
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending', verbose_name="订单状态")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总金额")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="所属订单")
    product_name = models.CharField(max_length=200, verbose_name="产品名称")
    quantity = models.PositiveIntegerField(verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")
    
    def __str__(self):
        return f'{self.product_name} x {self.quantity}'