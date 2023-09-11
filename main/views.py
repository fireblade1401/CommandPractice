from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout

from . import forms
from .models import Categories, Product, MainSlider, Cart, CartItem
from .forms import CallbackForm


# Create your views here.

def index(request):
    slides = MainSlider.objects.all()
    product_womans = Product.objects.filter(category=1)
    product_mans = Product.objects.filter(category=2)
    product_tech = Product.objects.filter(category=3)

    context = {
        'slides': slides,
        'product_tech': product_tech,
        'product_womans': product_womans,
        'product_mans': product_mans,

    }

    return render(request, 'main/index.html', context)


def computers(request):
    product_tech = Product.objects.filter(category=3)

    context = {
        'product_tech': product_tech,
    }

    return render(request, 'main/computers.html', context)


def mans_clothes(request):
    product_mans = Product.objects.filter(category=2)

    context = {
        'product_mans': product_mans,
    }

    return render(request, 'main/mans_clothes.html', context)


def womans_clothes(request):
    product_womans = Product.objects.filter(category=1)

    context = {
        'product_womans': product_womans,
    }

    return render(request, 'main/womans_clothes.html', context)


def contact(request):
    return render(request, 'main/contact.html')


def callback(request):
    if request.method == "POST":
        form = CallbackForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо за обращение, мы свяжемся с вами в ближайшее время!')
            return redirect('contact')

    else:
        form = CallbackForm()

    context = {
        'form': form,
    }

    return render(request, 'main/contact.html', context)


def profile(request):
    try:
        active_cart = Cart.objects.get(user=request.user, completed=False)
        cart_items = CartItem.objects.filter(cart=active_cart)

        context = {
            'items': cart_items,
            'total_price': sum(item.total_price for item in cart_items),
            'total_quantity': sum(item.quantity for item in cart_items)
        }
        return render(request, 'main/profile.html', context)
    except Cart.DoesNotExist:
        messages.error(request, "Корзина не найдена!")
        return render(request, 'main/profile.html', {})
    except Exception as e:
        messages.error(request, f"Произошла ошибка: {str(e)}")
        return render(request, 'main/profile.html', {})



def login_view(request):
    # Обработка данных формы входа
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()

    # Отправка формы в шаблон и отображение страницы входа
    return render(request, 'main/login.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'main/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def products(request):
    category = Categories.objects.all()
    products = Product.objects.all()

    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Фильтрация по цене
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(product_price__gte=min_price)
    if max_price:
        products = products.filter(product_price__lte=max_price)

    # Сортировка
    sort_by = request.GET.get('sort_by')
    if sort_by:
        products = products.order_by(sort_by)

    context = {
        'category': category,
        'products': products,
    }

    return render(request, 'main/products.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(user=request.user, completed=False)  # Только get, не get_or_create
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('profile')


def decrease_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created and cart_item.quantity > 0:
        cart_item.quantity -= 1
        cart_item.save()

        if cart_item.quantity == 0:
            cart_item.delete()

    return redirect('profile')


def place_order(request):
    try:
        active_cart = Cart.objects.get(user=request.user, completed=False)  # Найти активную корзину
        active_cart.completed = True  # Отметить корзину как завершенную (заказ)
        active_cart.save()

        # Создать новую корзину для пользователя
        Cart.objects.create(user=request.user)
        return redirect('products')
    except Cart.DoesNotExist:
        messages.error(request, "Корзина не найдена!")
        return redirect('products')
    except Exception as e:
        messages.error(request, f"Произошла ошибка: {str(e)}")
        return redirect('products')
