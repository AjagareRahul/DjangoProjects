"""
Raw Shop - E-commerce Application Views
========================================
This file contains all the views for the Raw Shop e-commerce application.
Views are organized by functionality: Authentication, Products, Cart, Orders, Wishlist, and Profile.
"""

# Django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Local imports - Models
from store.models import (
    Category, Product, Cart, CartItem, 
    Order, OrderItem, Wishlist, UserProfile
)

# Local imports - Forms
from store.forms import CheckoutForm, SignUpForm, LoginForm, UserProfileForm


# ============================================================================
# AUTHENTICATION VIEWS
# ============================================================================

def register_page(request):
    """
    Handle user registration.
    - GET: Display registration form
    - POST: Create new user account, profile, and cart
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                # Create user account
                user = form.save()
                
                # Create user profile and cart
                UserProfile.objects.get_or_create(user=user)
                Cart.objects.get_or_create(user=user)
                
                # Redirect to login page
                messages.success(request, 'Account created! Please login with your credentials.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            # Display form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})


def home_page(request):
    """
    Landing page.
    - Authenticated users -> Dashboard
    - Unauthenticated users -> Registration page
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'signup.html')


def login_page(request):
    """
    Handle user login.
    - GET: Display login form
    - POST: Authenticate user and redirect
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                # Redirect to 'next' parameter if exists, otherwise to dashboard
                next_url = request.GET.get('next')
                return redirect(next_url) if next_url else redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_page(request):
    """Log out user and redirect to login page."""
    logout(request)
    return redirect('login')


# ============================================================================
# PRODUCT VIEWS
# ============================================================================

@login_required
def product_list(request):
    """
    Display all products with category filtering.
    """
    products = Product.objects.all()
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    
    # Filter by category if selected
    if selected_category:
        try:
            selected_category_id = int(selected_category)
            products = products.filter(Category_id=selected_category_id)
            selected_category = selected_category_id
        except ValueError:
            selected_category = None
    
    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category
    })


@login_required
def product_detail(request, product_id):
    """Display detailed view of a single product."""
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_details.html', {'product': product})


# ============================================================================
# CART VIEWS
# ============================================================================

@login_required
def get_user_cart(user):
    """Get or create cart for a user."""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def add_to_cart(request, product_id):
    """
    Add a product to user's cart.
    - If product already in cart, increase quantity by 1
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create cart
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')


@login_required
def view_cart(request):
    """Display user's cart with items and total price."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate item totals
    for item in cart_items:
        item.item_total = item.product.price * item.quantity

    total = sum(item.item_total for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def update_cart(request, item_id, action):
    """
    Update cart item quantity.
    - 'inc': Increase quantity
    - 'dec': Decrease quantity (delete if becomes 0)
    """
    item = get_object_or_404(CartItem, id=item_id)

    if action == 'inc':
        item.quantity += 1
    elif action == 'dec':
        item.quantity -= 1
        if item.quantity == 0:
            item.delete()
            return redirect('cart_detail')

    item.save()
    return redirect('cart_detail')


@login_required
def remove_from_cart(request, item_id):
    """Remove an item from cart."""
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_detail')


# ============================================================================
# ORDER VIEWS
# ============================================================================

@login_required
def place_order(request):
    """Place order from cart items (without address)."""
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('cart_detail')

    # Calculate total price
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Create order
    order = Order.objects.create(
        user=request.user,
        total_price=total_price
    )

    # Create order items and clear cart
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()
    return redirect('order_success', order_id=order.id)


@login_required
def order_success(request, order_id):
    """Display order confirmation page."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)
    return render(request, 'order_success.html', {'order': order, 'items': items})


@login_required
def my_orders(request):
    """Display user's order history."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})


@login_required
def checkout(request):
    """
    Checkout process with address form.
    - Display cart items and total
    - Collect delivery address
    - Create order with address
    """
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if not cart_items.exists():
        return redirect('cart_detail')
    
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_price=total_price
            )
            
            # Save address
            address = form.save(commit=False)
            address.order = order
            address.save()
            
            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            # Clear cart
            cart_items.delete()
            return redirect('order_success', order_id=order.id)
    else:
        form = CheckoutForm()
    
    return render(request, 'checkout.html', {'form': form, 'total_price': total_price})


# ============================================================================
# WISHLIST VIEWS
# ============================================================================

@login_required
def add_to_wishlist(request, product_id):
    """
    Add a product to user's wishlist.
    - Prevents duplicate entries
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Check if already in wishlist
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        messages.success(request, f'{product.name} added to your wishlist!')
    else:
        messages.info(request, f'{product.name} is already in your wishlist')
    
    return redirect('product_details', product_id=product_id)


@login_required
def remove_from_wishlist(request, product_id):
    """Remove a product from user's wishlist."""
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product)
    
    if wishlist_item.exists():
        wishlist_item.delete()
        messages.success(request, f'{product.name} removed from your wishlist')
    
    return redirect('view_wishlist')


@login_required
def view_wishlist(request):
    """Display all products in user's wishlist."""
    wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-added_at')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


# ============================================================================
# BUY NOW VIEW - Direct checkout for single product
# ============================================================================

@login_required
def buy_now(request, product_id):
    """
    Direct checkout for a single product.
    - Requires address before placing order
    - Pre-fills form with saved profile data
    - Updates profile with new address after order
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Check stock
    if product.stock == 0:
        messages.error(request, 'This product is out of stock')
        return redirect('product_details', product_id=product_id)
    
    # Get quantity (default to 1)
    quantity = int(request.POST.get('quantity', 1))
    quantity = max(1, min(quantity, product.stock))
    
    total_price = product.price * quantity
    
    # Pre-fill form with user profile data
    initial_data = {}
    try:
        profile = UserProfile.objects.get(user=request.user)
        initial_data = {
            'address': profile.address or '',
            'city': profile.city or '',
            'pincode': profile.pincode or '',
            'phone': profile.phone or '',
        }
    except UserProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_price=total_price
            )
            
            # Create order item
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )
            
            # Save address
            address = form.save(commit=False)
            address.order = order
            address.save()
            
            # Update user profile with new address
            try:
                profile = UserProfile.objects.get(user=request.user)
                profile.phone = form.cleaned_data.get('phone', profile.phone)
                profile.address = form.cleaned_data.get('address', profile.address)
                profile.city = form.cleaned_data.get('city', profile.city)
                profile.pincode = form.cleaned_data.get('pincode', profile.pincode)
                profile.save()
            except UserProfile.DoesNotExist:
                pass
            
            messages.success(request, 'Order placed successfully!')
            return redirect('order_success', order_id=order.id)
    else:
        form = CheckoutForm(initial=initial_data)
    
    return render(request, 'buy_now_checkout.html', {
        'product': product,
        'quantity': quantity,
        'total_price': total_price,
        'form': form
    })


# ============================================================================
# PROFILE VIEWS
# ============================================================================

@login_required
def profile_view(request):
    """
    User profile management.
    - Display and edit user profile including address
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form})


@login_required
def dashboard(request):
    """
    User dashboard showing:
    - Order count
    - Wishlist count
    - Cart items count
    """
    # Get user stats
    orders_count = Order.objects.filter(user=request.user).count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    addresses_count = 0
    
    # Get cart items count
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items_count = CartItem.objects.filter(cart=cart).count()
    except Cart.DoesNotExist:
        cart_items_count = 0
    
    return render(request, 'dashboard.html', {
        'orders_count': orders_count,
        'wishlist_count': wishlist_count,
        'addresses_count': addresses_count,
        'cart_items_count': cart_items_count
    })
