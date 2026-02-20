"""
Django Signals for Portfolio Website
"""

from django.db.models.signals import post_save, post_delete, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from .models import UserActivity, VisitorCount, ContactMessage


@receiver(post_save, sender=User)
def create_user_activity_on_registration(sender, instance, created, **kwargs):
    """
    Create user activity when a new user is registered
    """
    if created:
        UserActivity.objects.create(
            user=instance,
            activity_type='register',
            description=f'New user registered: {instance.username}'
        )


@receiver(post_save, sender=ContactMessage)
def create_contact_activity(sender, instance, created, **kwargs):
    """
    Create user activity when a contact message is submitted
    """
    if created:
        # Try to get user if authenticated
        try:
            user = instance
        except Exception:
            user = None
        
        # Log the activity (we don't have user info from contact form)
        pass


def log_user_login(sender, request, user, **kwargs):
    """
    Log user login activity
    """
    UserActivity.objects.create(
        user=user,
        activity_type='login',
        description=f'User logged in',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:300]
    )


def log_user_logout(sender, request, user, **kwargs):
    """
    Log user logout activity
    """
    UserActivity.objects.create(
        user=user,
        activity_type='logout',
        description=f'User logged out',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:300]
    )


def get_client_ip(request):
    """
    Get client IP address from request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(post_save, sender=VisitorCount)
def update_visitor_count(sender, instance, created, **kwargs):
    """
    Update visitor count timestamp
    """
    if created:
        instance.last_visitor = timezone.now()
        instance.save()


@receiver(pre_save, sender=ContactMessage)
def sanitize_contact_message(sender, instance, **kwargs):
    """
    Sanitize contact message before saving
    """
    instance.name = instance.name.strip()
    instance.email = instance.email.strip().lower()
    instance.subject = instance.subject.strip()
    instance.message = instance.message.strip()
