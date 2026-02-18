from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, CartItem

# ---------- AUTH ----------

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid credentials")
            return redirect("cart:login")

        login(request, user)
        return redirect("cart:product_list")

    return render(request, "cart/login.html")


def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("cart:register")

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully")
        return redirect("cart:login")

    return render(request, "cart/register.html")


@login_required(login_url="cart:login")
def logout_page(request):
    logout(request)
    return redirect("cart:login")


# ---------- PRODUCTS ----------

def product_list(request):
    products = Product.objects.all()
    return render(request, "cart/index.html", {"products": products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "cart/product_detail.html", {"product": product})


# ---------- CART ----------

@login_required(login_url="cart:login")
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if product.stock <= cart_item.quantity:
        messages.error(request, "Stock not available")
        return redirect("cart:product_list")

    cart_item.quantity += 1
    cart_item.save()
    return redirect("cart:view_cart")


@login_required(login_url="cart:login")
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, "cart/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price
    })


@login_required(login_url="cart:login")
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user
    )
    cart_item.delete()
    return redirect("cart:view_cart")


# ---------- CHECKOUT ----------

@login_required(login_url="cart:login")
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, "cart/checkout.html", {
        "cart_items": cart_items,
        "total_price": total_price
    })
