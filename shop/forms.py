# shop/forms.py
from django import forms
from django.forms.models import inlineformset_factory
from .models import Order, OrderItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_number', 'customer_name', 'status', 'total_amount']

# 基于 Order 和 OrderItem 关系生成内联 FormSet
OrderItemFormSet = inlineformset_factory(
    Order, 
    OrderItem, 
    fields=['product_name', 'quantity', 'price'], 
    extra=1,            # 默认提供一行空白表单
    can_delete=True     # 支持删除功能
)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="邮箱")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    # 重写 save 方法，保存邮箱数据
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user