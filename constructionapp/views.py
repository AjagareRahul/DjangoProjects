from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Category, Product, CartItem, Order, OrderItem, UserProfile
from .forms import UserProfileForm
import json


def home(request):
    # Get all available products for display
    cement_products = Product.objects.filter(category='cement', is_available=True)[:6]
    sand_products = Product.objects.filter(category='sand', is_available=True)[:6]
    steel_products = Product.objects.filter(category='steel', is_available=True)[:6]
    brick_products = Product.objects.filter(category='brick', is_available=True)[:6]
    
    # Get all featured products
    featured_products = Product.objects.filter(is_available=True)[:12]
    
    # Define categories for display
    categories_list = [
        {'name': 'Cement', 'slug': 'cement', 'icon': 'fa-cubes', 'description': 'OPC, PPC, White Cement & more'},
        {'name': 'Sand', 'slug': 'sand', 'icon': 'fa-mountain', 'description': 'River Sand, M-Sand, Plastering Sand'},
        {'name': 'Steel', 'slug': 'steel', 'icon': 'fa-industry', 'description': 'TMT Bars, Fe 415, Fe 500, Fe 550'},
        {'name': 'Bricks', 'slug': 'brick', 'icon': 'fa-th-large', 'description': 'Red Bricks, Fly Ash, Concrete Blocks'},
        {'name': 'Aggregates', 'slug': 'aggregate', 'icon': 'fa-cubes-stacked', 'description': '20mm, 10mm, Gitti'},
        {'name': 'Hardware', 'slug': 'hardware', 'icon': 'fa-tools', 'description': 'Plywood, Binding Wire & more'},
    ]
    
    context = {
        'categories': categories_list,
        'cement_products': cement_products,
        'sand_products': sand_products,
        'steel_products': steel_products,
        'brick_products': brick_products,
        'featured_products': featured_products,
    }
    return render(request, 'constructionapp/home.html', context)


def product_list(request, category=None):
    if category:
        products = Product.objects.filter(category=category, is_available=True)
        category_name = category.capitalize()
    else:
        products = Product.objects.filter(is_available=True)
        category_name = 'All Products'
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category,
        'category_name': category_name,
    }
    return render(request, 'constructionapp/product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'constructionapp/product_detail.html', context)


def cart(request):
    cart_items = get_cart_items(request)
    total = calculate_cart_total(request)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'constructionapp/cart.html', context)


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity < 1:
        quantity = 1
    
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        cart_item, created = CartItem.objects.get_or_create(
            session_key=session_key,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart')


@require_POST
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity < 1:
        cart_item.delete()
    else:
        cart_item.quantity = quantity
        cart_item.save()
    
    return redirect('cart')


@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')
    
    total = sum(item.get_total_price() for item in cart_items)
    
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        notes = request.POST.get('notes', '')
        
        if not shipping_address or not phone or not email:
            messages.error(request, 'Please fill in all required fields!')
        else:
            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                shipping_address=shipping_address,
                phone=phone,
                email=email,
                notes=notes,
                status='CONFIRMED'
            )
            
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            cart_items.delete()
            messages.success(request, f'Order placed successfully! Order number: {order.order_number}')
            return redirect('order_confirmation', order_id=order.id)
    
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'profile': profile,
    }
    return render(request, 'constructionapp/checkout.html', context)


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'constructionapp/order_confirmation.html', context)


@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user)[:10]
    
    # Get products for quick shopping
    cement_products = Product.objects.filter(category='cement', is_available=True)[:4]
    sand_products = Product.objects.filter(category='sand', is_available=True)[:4]
    steel_products = Product.objects.filter(category='steel', is_available=True)[:4]
    brick_products = Product.objects.filter(category='brick', is_available=True)[:4]
    all_products = Product.objects.filter(is_available=True)[:8]
    
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    context = {
        'user': request.user,
        'profile': profile,
        'orders': orders,
        'cement_products': cement_products,
        'sand_products': sand_products,
        'steel_products': steel_products,
        'brick_products': brick_products,
        'all_products': all_products,
    }
    return render(request, 'constructionapp/dashboard.html', context)


@login_required
def profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
    }
    return render(request, 'constructionapp/profile.html', context)


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    
    context = {
        'orders': orders,
    }
    return render(request, 'constructionapp/order_history.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'constructionapp/login.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'constructionapp/register.html',)


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out!')
    return redirect('home')


def search_products(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query, is_available=True)
    else:
        products = Product.objects.none()
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'constructionapp/search_results.html', context)


def get_cart_items(request):
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        return CartItem.objects.filter(session_key=session_key)


def calculate_cart_total(request):
    cart_items = get_cart_items(request)
    return sum(item.get_total_price() for item in cart_items)
