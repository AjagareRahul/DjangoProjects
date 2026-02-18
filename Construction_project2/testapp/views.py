from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required

from testapp.models import Material, Cart, CartItem, Order, OrderItem
from testapp.forms import (MaterialForm,LoginForm,RegistrationForm,UserUpdateForm,ProfileUpdateForm)

# ---------------- HOME ----------------
@login_required
def home(request):
    items = Material.objects.all()
    return render(request, 'home.html', {'items': items})


# ---------------- AUTH ----------------
def registerform(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'registration.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            auth_login(request, user)
            return redirect('home')
        form.add_error(None, "Invalid username or password")
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------- MATERIAL CRUD ----------------
@login_required
def add_items(request):
    form = MaterialForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('home')

    items = Material.objects.all()
    return render(request, 'home.html', {'form': form, 'items': items})


@login_required
def update_items(request, id):
    material = get_object_or_404(Material, id=id)
    form = MaterialForm(request.POST or None, instance=material)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'update_items.html', {'form': form})


@login_required
def delete(request, id):
    material = get_object_or_404(Material, id=id)
    material.delete()
    return redirect('home')


# ---------------- CART ----------------
@login_required
def add_to_cart(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    quantity = int(request.POST.get('quantity', 1))
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        material=material
    )

    cart_item.quantity = cart_item.quantity + quantity if not created else quantity
    cart_item.save()

    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})


@login_required
def increase_qty(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.quantity += 1
    item.save()
    return redirect('view_cart')


@login_required
def decrease_qty(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('view_cart')


@login_required
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('view_cart')


# ---------------- CHECKOUT & ORDER ----------------
@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)

    if not cart.cartitem_set.exists():
        return redirect('home')

    if request.method == "POST":
        address = request.POST.get('address')
        total = cart.grand_total()

        order = Order.objects.create(
            user=request.user,
            address=address,
            total_amount=total
        )

        for item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                material=item.material,
                price=item.material.price,
                quantity=item.quantity
            )

            # Reduce stock
            item.material.stock -= item.quantity
            item.material.save()

        cart.cartitem_set.all().delete()
        return redirect('order_success')

    return render(request, 'checkout.html', {'cart': cart})


@login_required
def order_success(request):
    return render(request, 'order_success.html')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})


# ---------------- PROFILE ----------------
@login_required
def profile(request):
    user_form = UserUpdateForm(
        request.POST or None,
        instance=request.user
    )

    profile_form = ProfileUpdateForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user.userprofile
    )

    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
