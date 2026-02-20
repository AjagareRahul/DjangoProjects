"""
Custom Context Processors for Rahul Portfolio Website
"""

from django.shortcuts import get_object_or_404
from portfolio.models import SiteInfo, SocialLink, Skill, Project


def site_info(request):
    """
    Context processor to make site information available globally
    """
    try:
        site_info = SiteInfo.objects.first()
    except SiteInfo.DoesNotExist:
        site_info = None
    
    return {
        'site_info': site_info,
    }


def social_links(request):
    """
    Context processor to make social links available globally
    """
    try:
        social_links = SocialLink.objects.filter(is_active=True)
    except SocialLink.DoesNotExist:
        social_links = []
    
    return {
        'social_links': social_links,
    }


def visitor_count(request):
    """
    Context processor to make visitor count available globally
    """
    try:
        from portfolio.models import VisitorCount
        visitor = VisitorCount.objects.get(id=1)
        visitor_count = visitor.count
    except VisitorCount.DoesNotExist:
        visitor_count = 0
    except Exception:
        visitor_count = 0
    
    return {
        'visitor_count': visitor_count,
    }


def featured_skills(request):
    """
    Context processor to make featured skills available globally
    """
    try:
        skills = Skill.objects.filter(is_active=True).order_by('-proficiency')[:6]
    except Skill.DoesNotExist:
        skills = []
    
    return {
        'featured_skills': skills,
    }


def recent_projects(request):
    """
    Context processor to make recent projects available globally
    """
    try:
        projects = Project.objects.filter(is_published=True).order_by('-created_at')[:3]
    except Project.DoesNotExist:
        projects = []
    
    return {
        'recent_projects': recent_projects,
    }
