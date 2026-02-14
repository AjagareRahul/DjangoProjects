from .views import get_cart_items, calculate_cart_total


def cart_total(request):
    """Add cart total to all template contexts"""
    total = calculate_cart_total(request)
    item_count = get_cart_items(request).count()
    return {
        'cart_total': total,
        'cart_item_count': item_count,
    }
