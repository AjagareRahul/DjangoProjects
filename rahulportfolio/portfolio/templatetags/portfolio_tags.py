"""
Custom Template Tags and Filters for Portfolio Website
"""

from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
import re

register = template.Library()


# ==================== Custom Filters ====================

@register.filter
@stringfilter
def truncatewords_custom(value, arg):
    """
    Custom truncate words filter
    """
    try:
        length = int(arg)
    except ValueError:
        return value
    
    if len(value) <= length:
        return value
    
    return value[:length] + '...'


@register.filter
def get_item(dictionary, key):
    """
    Get item from dictionary by key
    """
    return dictionary.get(key)


@register.filter
def split_by_comma(value):
    """
    Split a string by comma and return a list
    """
    if not value:
        return []
    return [item.strip() for item in value.split(',')]


@register.filter
def star_rating(value):
    """
    Convert numeric rating to star icons
    """
    try:
        rating = int(value)
    except (ValueError, TypeError):
        rating = 0
    
    stars = '★' * rating + '☆' * (5 - rating)
    return mark_safe(f'<span class="text-warning">{stars}</span>')


@register.filter
def time_ago(value):
    """
    Convert datetime to time ago string
    """
    from django.utils import timezone
    from datetime import timedelta
    
    if not value:
        return ''
    
    now = timezone.now()
    diff = now - value
    
    if diff.days > 365:
        years = diff.days // 365
        return f'{years} year{"s" if years > 1 else ""} ago'
    elif diff.days > 30:
        months = diff.days // 30
        return f'{months} month{"s" if months > 1 else ""} ago'
    elif diff.days > 0:
        return f'{diff.days} day{"s" if diff.days > 1 else ""} ago'
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f'{hours} hour{"s" if hours > 1 else ""} ago'
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
    else:
        return 'Just now'


@register.filter
def add_class(field, css_class):
    """
    Add CSS class to form field
    """
    return field.as_widget(attrs={"class": css_class})


@register.filter
def format_technology(tech_string):
    """
    Format technology string as badges
    """
    if not tech_string:
        return ''
    
    technologies = [t.strip() for t in tech_string.split(',')]
    badges = []
    
    tech_colors = {
        'python': 'bg-primary',
        'django': 'bg-success',
        'javascript': 'bg-warning text-dark',
        'html': 'bg-danger',
        'css': 'bg-info text-dark',
        'react': 'bg-primary',
        'vue': 'bg-success',
        'angular': 'bg-danger',
        'node': 'bg-success',
        'sql': 'bg-warning text-dark',
        'postgresql': 'bg-primary',
        'mysql': 'bg-warning text-dark',
        'mongodb': 'bg-success',
        'docker': 'bg-info text-dark',
        'git': 'bg-secondary',
    }
    
    for tech in technologies:
        tech_lower = tech.lower()
        color_class = tech_colors.get(tech_lower, 'bg-secondary')
        badges.append(f'<span class="badge {color_class} me-1">{tech}</span>')
    
    return mark_safe(' '.join(badges))


# ==================== Custom Tags ====================

@register.simple_tag
def get_social_icon(platform):
    """
    Get Font Awesome icon class for social platform
    """
    icons = {
        'github': 'fab fa-github',
        'linkedin': 'fab fa-linkedin',
        'twitter': 'fab fa-twitter',
        'instagram': 'fab fa-instagram',
        'facebook': 'fab fa-facebook',
        'youtube': 'fab fa-youtube',
        'stackoverflow': 'fab fa-stack-overflow',
        'medium': 'fab fa-medium',
        'blog': 'fas fa-blog',
    }
    return icons.get(platform, 'fas fa-link')


@register.simple_tag
def get_skill_icon(skill_name):
    """
    Get Font Awesome icon for skill
    """
    skill_icons = {
        'python': 'fab fa-python',
        'django': 'fas fa-code',
        'javascript': 'fab fa-js',
        'html': 'fab fa-html5',
        'css': 'fab fa-css3-alt',
        'react': 'fab fa-react',
        'vue': 'fab fa-vuejs',
        'angular': 'fab fa-angular',
        'node': 'fab fa-node-js',
        'sql': 'fas fa-database',
        'docker': 'fab fa-docker',
        'git': 'fab fa-git-alt',
    }
    
    skill_lower = skill_name.lower()
    for key, icon in skill_icons.items():
        if key in skill_lower:
            return icon
    
    return 'fas fa-code'


@register.inclusion_tag('portfolio/tags/skills_progress.html')
def render_skills_progress(skills):
    """
    Render skills with progress bars
    """
    return {'skills': skills}


@register.inclusion_tag('portfolio/tags/project_card.html')
def render_project_card(project):
    """
    Render project card
    """
    return {'project': project}


@register.inclusion_tag('portfolio/tags/testimonial_card.html')
def render_testimonial_card(testimonial):
    """
    Render testimonial card
    """
    return {'testimonial': testimonial}


@register.inclusion_tag('portfolio/tags/message_alert.html')
def show_messages(messages):
    """
    Render Django messages as Bootstrap alerts
    """
    return {'messages': messages}


@register.simple_tag
def get_site_version():
    """
    Get site version
    """
    return '1.0.0'


@register.simple_tag
def get_current_year():
    """
    Get current year
    """
    from django.utils import timezone
    return timezone.now().year


@register.simple_tag
def url_replace(request, field, value):
    """
    Replace URL parameter and return new URL
    """
    from django.utils.http import urlencode
    dict_ = request.GET.copy()
    dict_[field] = value
    return urlencode(dict_)
