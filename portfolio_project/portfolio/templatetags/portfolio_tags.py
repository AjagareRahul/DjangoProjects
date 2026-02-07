"""
Custom template tags for portfolio app.
"""

from django import template

register = template.Library()


@register.simple_tag
def split_technologies(technologies, delimiter=','):
    """Split a comma-separated string into a list."""
    if not technologies:
        return []
    return [t.strip() for t in technologies.split(delimiter)]
