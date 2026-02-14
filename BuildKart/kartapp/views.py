from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Avg, Count
from .models import (
    Category, Brand, Product, ProductReview, CartItem, 
    Wishlist, Address, Order, OrderItem, UserProfile, Testimonial
)
from .forms import UserProfileForm, AddressForm
import random


def home_redirect(request):
    """Redirect authenticated users to dashboard, show welcome to others"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def home(request):
    """Homepage with categories, featured products, testimonials"""
    categories = Category.objects.filter(is_active=True)[:8]
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:12]
    best_sellers = Product.objects.filter(is_active=True).annotate(
        order_count=Count('orderitem')
    ).order_by('-order_count')[:8]
    testimonials = Testimonial.objects.filter(is_active=True)[:5]
    
    # Get products by category
    cement_products = Product.objects.filter(category__slug='cement', is_active=True)[:4]
    steel_products = Product.objects.filter(category__slug='steel', is_active=True)[:4]
    bricks_products = Product.objects.filter(category__slug='bricks', is_active=True)[:4]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'best_sellers': best_sellers,
        'testimonials': testimonials,
        'cement_products': cement_products,
        'steel_products': steel_products,
        'bricks_products': bricks_products,
    }
    return render(request, 'kartapp/home.html', context)


def product_list(request, category_slug=None):
    """Product listing with filters"""
    category = None
    categories = Category.objects.filter(is_active=True)
    
    # Get filter parameters
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'newest')
    brand_filter = request.GET.get('brand', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    in_stock = request.GET.get('in_stock', '')
    
    products = Product.objects.filter(is_active=True)
    
    # Category filter
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Search filter
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(brand__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Brand filter
    if brand_filter:
        products = products.filter(brand__slug=brand_filter)
    
    # Price filter
    if min_price:
        products = products.filter(price__gte=float(min_price))
    if max_price:
        products = products.filter(price__lte=float(max_price))
    
    # Stock filter
    if in_stock:
        products = products.filter(stock__gt=0)
    
    # Sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')
    
    # Get brands for filter
    brands = Brand.objects.filter(is_active=True, products__in=products).distinct()
    
    context = {
        'products': products,
        'categories': categories,
        'category': category,
        'brands': brands,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'kartapp/product_list.html', context)


def product_detail(request, product_id):
    """Product detail page"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:8]
    reviews = ProductReview.objects.filter(product=product).order_by('-created_at')[:5]
    
    # Check if in wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(
            user=request.user, 
            product=product
        ).exists()
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'kartapp/product_detail.html', context)


@require_POST
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity < product.min_order_quantity:
        quantity = product.min_order_quantity
    
    if product.stock < quantity:
        return JsonResponse({
            'success': False, 
            'message': 'Sorry, required quantity not available in stock'
        })
    
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
    
    cart_count = get_cart_count(request)
    return JsonResponse({
        'success': True, 
        'message': f'{product.name} added to cart!',
        'cart_count': cart_count
    })


def cart(request):
    """Shopping cart page"""
    cart_items = get_cart_items(request)
    subtotal = sum(item.get_total_price() for item in cart_items)
    shipping = 0 if subtotal >= 5000 else 500
    tax = (subtotal * 0.18)  # 18% GST
    total = subtotal + shipping + tax
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
    }
    return render(request, 'kartapp/cart.html', context)


@require_POST
def update_cart(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity < 1:
        cart_item.delete()
        messages.success(request, 'Item removed from cart!')
    else:
        if quantity <= cart_item.product.stock:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated!')
        else:
            messages.error(request, 'Requested quantity not available!')
    
    return redirect('cart')


@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')


@login_required
def checkout(request):
    """Checkout page"""
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')
    
    subtotal = sum(item.get_total_price() for item in cart_items)
    shipping = 0 if subtotal >= 5000 else 500
    tax = (subtotal * 0.18)
    total = subtotal + shipping + tax
    
    addresses = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
        address_id = request.POST.get('address')
        payment_method = request.POST.get('payment_method', 'cod')
        
        try:
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            messages.error(request, 'Please select a shipping address!')
            return redirect('checkout')
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_address=address,
            payment_method=payment_method,
            subtotal=subtotal,
            shipping_cost=shipping,
            tax=tax,
            total=total,
            status='confirmed'
        )
        
        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                total=item.get_total_price()
            )
            # Reduce stock
            item.product.stock -= item.quantity
            item.product.save()
        
        # Clear cart
        cart_items.delete()
        
        messages.success(request, f'Order placed successfully! Order #{order.order_number}')
        return redirect('order_confirmation', order_id=order.id)
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
        'addresses': addresses,
    }
    return render(request, 'kartapp/checkout.html', context)


def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'kartapp/order_confirmation.html', {'order': order})


@login_required
def dashboard(request):
    """User dashboard"""
    orders = Order.objects.filter(user=request.user)[:5]
    wishlist = Wishlist.objects.filter(user=request.user)[:6]
    addresses = Address.objects.filter(user=request.user)[:3]
    
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = None
    
    context = {
        'orders': orders,
        'wishlist': wishlist,
        'addresses': addresses,
        'profile': profile,
    }
    return render(request, 'kartapp/dashboard.html', context)


@login_required
def orders(request):
    """Order history"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'kartapp/orders.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """Order detail page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'kartapp/order_detail.html', {'order': order})


@login_required
def wishlist(request):
    """User wishlist"""
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'kartapp/wishlist.html', {'wishlist_items': wishlist_items})


@require_POST
@login_required
def add_to_wishlist(request, product_id):
    """Add to wishlist"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        messages.success(request, f'{product.name} added to wishlist!')
    else:
        messages.info(f'{product.name} is already in your wishlist!')
    
    return redirect('wishlist')


@require_POST
@login_required
def remove_from_wishlist(request, product_id):
    """Remove from wishlist"""
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    messages.success(request, 'Item removed from wishlist!')
    return redirect('wishlist')


@login_required
def addresses(request):
    """User addresses"""
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'kartapp/addresses.html', {'addresses': addresses})


@login_required
def add_address(request):
    """Add new address"""
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully!')
            return redirect('addresses')
    else:
        form = AddressForm()
    
    return render(request, 'kartapp/add_address.html', {'form': form})


@login_required
def edit_address(request, address_id):
    """Edit address"""
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully!')
            return redirect('addresses')
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'kartapp/edit_address.html', {'form': form, 'address': address})


@login_required
def delete_address(request, address_id):
    """Delete address"""
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted!')
    return redirect('addresses')


@login_required
def profile(request):
    """User profile"""
    try:
        profile = request.user.profile
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
    
    return render(request, 'kartapp/profile.html', {'form': form})


def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password!')
    else:
        form = AuthenticationForm()
    
    return render(request, 'kartapp/login.html', {'form': form})


def register(request):
    """Registration page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
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
    
    return render(request, 'kartapp/register.html', {'form': form})


def logout_view(request):
    """Logout"""
    logout(request)
    messages.info(request, 'You have been logged out!')
    return redirect('home')


def search(request):
    """Global search"""
    query = request.GET.get('q', '')
    products = []
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(description__icontains=query),
            is_active=True
        )[:20]
    
    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'kartapp/search.html', context)


# Helper functions
def get_cart_items(request):
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        return CartItem.objects.filter(session_key=session_key)


def get_cart_count(request):
    cart_items = get_cart_items(request)
    return sum(item.quantity for item in cart_items)


def cart_context(request):
    """Context processor for cart"""
    cart_count = get_cart_count(request)
    cart_total = sum(item.get_total_price() for item in get_cart_items(request))
    return {'cart_count': cart_count, 'cart_total': cart_total}
