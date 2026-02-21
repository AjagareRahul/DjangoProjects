from django.urls import path
from .views import *

urlpatterns = [
    # Landing page - shows register for unauthenticated, dashboard for authenticated
    path("", home_page, name="home"),
    path("products/", product_list, name="product_list"),
    path("product/<int:product_id>/", product_detail, name="product_details"),

    # Authentication
    path("login/", login_page, name="login"),
    path("register/", register_page, name="sing_up"),
    path("logout/", logout_page, name="logout"),

    # Cart
    path("add-to-cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", view_cart, name="cart_detail"),
    path("update-cart/<int:item_id>/<str:action>/", update_cart, name="update_cart"),
    path("remove-from-cart/<int:item_id>/", remove_from_cart, name="remove_from_cart"),

    # Checkout
    path("checkout/", checkout, name="checkout"),
    path("order-success/<int:order_id>/", order_success, name="order_success"),
    path("my-orders/", my_orders, name="my_orders"),
    
    # Buy Now - Direct checkout
    path("buy-now/<int:product_id>/", buy_now, name="buy_now"),
    
    # Wishlist
    path("wishlist/", view_wishlist, name="view_wishlist"),
    path("add-to-wishlist/<int:product_id>/", add_to_wishlist, name="add_to_wishlist"),
    path("remove-from-wishlist/<int:product_id>/", remove_from_wishlist, name="remove_from_wishlist"),
    
    # Profile
    path("profile/", profile_view, name="profile"),
    path("dashboard/", dashboard, name="dashboard"),
]
