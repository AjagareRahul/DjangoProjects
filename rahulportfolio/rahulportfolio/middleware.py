"""
Custom Middleware for Rahul Portfolio Website
"""

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User
from django.utils import timezone
from portfolio.models import VisitorCount, UserActivity


class VisitorCountMiddleware(MiddlewareMixin):
    """
    Middleware to track visitor count
    """
    
    def process_request(self, request):
        # Get or create visitor count
        visitor_count, created = VisitorCount.objects.get_or_create(
            id=1,
            defaults={'count': 0}
        )
        
        # Only count unique page views (home page)
        if request.path == '/' or request.path == '':
            visitor_count.count += 1
            visitor_count.save()
        
        # Store visitor count in request for access in views
        request.visitor_count = visitor_count.count
        
        return None


class LastVisitMiddleware(MiddlewareMixin):
    """
    Middleware to track user's last visit using cookies and sessions
    """
    
    def process_request(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Get last visit from session
            last_visit = request.session.get('last_visit')
            
            # Update last visit time
            request.session['last_visit'] = str(timezone.now())
            
            # Log user activity
            if last_visit:
                UserActivity.objects.create(
                    user=request.user,
                    activity_type='visit',
                    description=f'User visited at {timezone.now()}'
                )
        
        return None
    
    def process_response(self, request, response):
        # Set a cookie to remember the visitor
        if not request.user.is_authenticated:
            # Set last visit cookie if not set
            if 'last_visit' not in request.COOKIES:
                response.set_cookie('last_visit', str(timezone.now()), max_age=60*60*24*365)
        
        return response
