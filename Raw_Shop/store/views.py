from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm
from store.models import Category, Product, Cart, CartItem, Order,OrderItem
from store.forms import CheckoutForm, SignUpForm, LoginForm, UserProfileForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import UserProfile


def register_page(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Use get_or_create to avoid UNIQUE constraint error
            UserProfile.objects.get_or_create(user=user)
            # Auto-login after registration
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('dashboard')
    else:
        form=SignUpForm()   
    return render(request,'signup.html',{'form':form})


def home_page(request):
    """Landing page - shows register for unauthenticated, dashboard for authenticated"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'signup.html')

def login_page(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect('dashboard')
            else:
                messages.error(request,'Invalid username or password')
    else:
        form=LoginForm()
    return render(request,'login.html',{'form':form})

def logout_page(request):
    logout(request)
    return redirect('/login/')
@login_required
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    
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
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_details.html', {'product': product})

@login_required
def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create the user's cart safely
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    # Get or create the cart item
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
    # Get or create the user's cart safely
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    
    cart_items = CartItem.objects.filter(cart=cart)

    # Add item_total to each item for template use
    for item in cart_items:
        item.item_total = item.product.price * item.quantity

    total = sum(item.item_total for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def update_cart(request, item_id, action):
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
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_detail')

@login_required
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('cart_detail')

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    order = Order.objects.create(
        user=request.user,
        total_price=total_price
    )

    # Clear the cart after placing the order
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


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)
    return render(request, 'order_success.html', {'order': order,'items': items
    })


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {
        'orders': orders
    })
@login_required
def checkout(request):
    cart=get_object_or_404(Cart,user=request.user)
    cart_items=CartItem.objects.filter(cart=cart)
    
    if not cart_items.exists():
        return redirect('cart_detail')
    total_price=sum(item.product.price*item.quantity for item in cart_items)
    
    if request.method=='POST':
        form=CheckoutForm(request.POST)
        if form.is_valid():
            order=Order.objects.create(
                user=request.user,
                total_price=total_price)
            address=form.save(commit=False)
            address.order=order
            address.save()
            
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart_items.delete()
            return redirect('order_success',order_id=order.id)
    else:
        form=CheckoutForm()
    return render(request,'checkout.html',{'form':form,'total_price':total_price})

@login_required
def profile_view(request):
    # Get or create the user profile if it doesn't exist
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
    # Get user stats
    orders_count = Order.objects.filter(user=request.user).count()
    # For now, wishlist and addresses are placeholders
    wishlist_count = 0
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
