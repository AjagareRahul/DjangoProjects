from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_order_confirmation_email(user, order, items):
    subject = f"Order Confirmation - Order #{order.id}"
    from_email = settings.EMAIL_HOST_USER
    to = [user.email]

    # Plain text (fallback)
    text_content = f"""
Hello {user.username},

Your order has been placed successfully 🎉

Order ID: {order.id}
Total Amount: ₹{order.total_price}

Thank you for shopping with us!
"""

    # HTML content
    html_content = render_to_string(
        'emails/order_confirmation.html',
        {
            'user': user,
            'order': order,
            'items': items
        }
    )

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()


def send_order_status_email(order):
    user = order.user

    subject = f"Order #{order.id} Status Updated"
    from_email = settings.EMAIL_HOST_USER
    to = [user.email]

    text_content = f"""
Hello {user.username},

Your order #{order.id} status is now {order.status}.
Total Amount: ₹{order.total_price}
"""

    html_content = render_to_string(
        'emails/order_status_email.html',
        {
            'user': user,
            'order': order
        }
    )

    email = EmailMultiAlternatives(subject, text_content, from_email, to)
    email.attach_alternative(html_content, "text/html")
    email.send()
