from .models import Category
from .views import get_cart_items, get_cart_count


def categories(request):
    """Add categories to all templates"""
    categories = Category.objects.filter(is_active=True)
    return {'all_categories': categories}


def cart_context(request):
    """Add cart info to all templates"""
    cart_items = get_cart_items(request)
    cart_count = sum(item.quantity for item in cart_items)
    cart_total = sum(item.get_total_price() for item in cart_items)
    return {'cart_count': cart_count, 'cart_total': cart_total}
