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


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="密码",
        widget=forms.PasswordInput,
        help_text="密码至少6位",
    )
    password2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput,
        help_text="请再次输入相同的密码",
    )

    class Meta:
        model = User
        # 这里只用到 username 字段，作为昵称
        fields = ("username",)
        labels = {
            "username": "昵称",
        }
        help_texts = {
            "username": "请输入昵称，昵称不能重复",
        }

    def clean_username(self):
        """
        校验昵称是否已经存在
        """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("该昵称已被注册，请选择其他昵称")
        return username

    def clean(self):
        """
        校验两次输入的密码是否一致，且密码至少6位
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error("password2", "两次输入的密码不一致")
            if len(password1) < 6:
                self.add_error("password1", "密码至少6位")
        return cleaned_data

    def save(self, commit=True):
        """
        保存用户时使用 set_password 方法对密码进行加密保存
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user