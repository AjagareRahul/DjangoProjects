from django.urls import path
from testapp.views import *

urlpatterns = [
    path('', home, name='root'),      # 👈 FIRST HOME PAGE
    path('home/', home, name='home'),

    path('registration/', registerform, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Material CRUD
    path('add_product/', add_items, name='add_product'),
    path('update_items/<int:id>/', update_items, name="update_items"),
    path('delete/<int:id>/', delete, name='delete'),

    # Cart
    path('add-to-cart/<int:material_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/increase/<int:item_id>/', increase_qty, name='increase_qty'),
    path('cart/decrease/<int:item_id>/', decrease_qty, name='decrease_qty'),
    path('cart/remove/<int:item_id>/', remove_item, name='remove_item'),

    # Order
    path('checkout/', checkout, name='checkout'),
    path('order-success/', order_success, name='order_success'),
    path('my-orders/', my_orders, name='my_orders'),
    
   path('profile/', profile, name='profile'),

]
