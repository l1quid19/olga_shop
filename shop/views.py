from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .models import Product, Category, Order, OrderItem, OrderStatusHistory, LoginAttempt
from .forms import SecureLoginForm

def index(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'shop/index.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    request.session['cart'] = cart
    return redirect('cart_view')

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        item_total = product.price * quantity
        total_price += item_total
        cart_items.append({'product': product, 'quantity': quantity, 'total': item_total})
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('index')
        
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            phone=phone,
            address=address,
            status='created'
        )
        
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(order=order, product=product, price=product.price, quantity=quantity)
            product.stock -= quantity
            product.save()
            
        OrderStatusHistory.objects.create(order=order, old_status='', new_status='created', changed_by=request.user)
        request.session['cart'] = {}
        return redirect('profile')
        
    return render(request, 'shop/checkout.html')

def profile(request):
    # Берем все заказы текущего пользователя
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/profile.html', {'orders': orders})

# Класс для защиты от Brute Force
class SecureLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = SecureLoginForm

    def form_invalid(self, form):
        # Если пароль неверный, записываем неудачную попытку
        username = form.cleaned_data.get('username')
        ip = self.request.META.get('REMOTE_ADDR')
        LoginAttempt.objects.create(username=username, ip_address=ip, is_success=False)
        return super().form_invalid(form)

    def form_valid(self, form):
        # Если вход успешный, записываем это и очищаем историю неудач
        username = form.cleaned_data.get('username')
        ip = self.request.META.get('REMOTE_ADDR')
        LoginAttempt.objects.create(username=username, ip_address=ip, is_success=True)
        # Удаляем старые неудачные попытки для этого пользователя
        LoginAttempt.objects.filter(username=username, is_success=False).delete()
        return super().form_valid(form)