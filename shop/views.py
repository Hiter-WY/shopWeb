# shop/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from .forms import OrderForm, OrderItemFormSet
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

# 首页视图（可作为登录后跳转页面）
def home(request):
    return render(request, 'shop/home.html')

# 用户注册视图
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 可选：注册成功后自动登录
            login(request, user)
            return redirect("home")  # 或跳转到其他页面
    else:
        form = CustomUserCreationForm()
    return render(request, "shop/register.html", {"form": form})
# 用户登录视图
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # 获取经过验证的用户对象
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})

# 用户登出视图
def user_logout(request):
    logout(request)
    return redirect('home')

# 订单列表
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'shop/order_list.html', {'orders': orders})

# 订单详情
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'shop/order_detail.html', {'order': order})

# 新建订单
def order_create(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if order_form.is_valid() and formset.is_valid():
            order = order_form.save()
            # 将表单集合中的每个明细保存，并关联到订单
            items = formset.save(commit=False)
            for item in items:
                item.order = order
                item.save()
            return redirect('order_list')
    else:
        order_form = OrderForm()
        formset = OrderItemFormSet()
    return render(request, 'shop/order_form.html', {'order_form': order_form, 'formset': formset})

# 编辑订单
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order_form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if order_form.is_valid() and formset.is_valid():
            order_form.save()
            formset.save()
            return redirect('order_list')
    else:
        order_form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)
    return render(request, 'shop/order_form.html', {'order_form': order_form, 'formset': formset})

# 删除订单
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect('order_list')
    return render(request, 'shop/order_confirm_delete.html', {'order': order})
