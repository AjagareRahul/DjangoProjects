from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # Home - Redirects to dashboard if authenticated, else shows home/welcome
    path('', views.home_redirect, name='home'),
    
    # Products - Protected (requires login)
    path('products/', login_required(views.product_list), name='product_list'),
    path('products/<slug:category_slug>/', login_required(views.product_list), name='product_list_by_category'),
    path('product/<int:product_id>/', login_required(views.product_detail), name='product_detail'),
    
    # Search - Protected
    path('search/', login_required(views.search), name='search'),
    
    # Cart - Protected
    path('cart/', login_required(views.cart), name='cart'),
    path('cart/add/<int:product_id>/', login_required(views.add_to_cart), name='add_to_cart'),
    path('cart/update/<int:item_id>/', login_required(views.update_cart), name='update_cart'),
    path('cart/remove/<int:item_id>/', login_required(views.remove_from_cart), name='remove_from_cart'),
    
    # Checkout - Protected
    path('checkout/', login_required(views.checkout), name='checkout'),
    path('order/confirmation/<int:order_id>/', login_required(views.order_confirmation), name='order_confirmation'),
    
    # User Dashboard - Protected
    path('dashboard/', login_required(views.dashboard), name='dashboard'),
    path('orders/', login_required(views.orders), name='orders'),
    path('order/<int:order_id>/', login_required(views.order_detail), name='order_detail'),
    path('wishlist/', login_required(views.wishlist), name='wishlist'),
    path('wishlist/add/<int:product_id>/', login_required(views.add_to_wishlist), name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', login_required(views.remove_from_wishlist), name='remove_from_wishlist'),
    path('addresses/', login_required(views.addresses), name='addresses'),
    path('address/add/', login_required(views.add_address), name='add_address'),
    path('address/edit/<int:address_id>/', login_required(views.edit_address), name='edit_address'),
    path('address/delete/<int:address_id>/', login_required(views.delete_address), name='delete_address'),
    path('profile/', login_required(views.profile), name='profile'),
    
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
