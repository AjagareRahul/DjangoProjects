"""
Views for portfolio app.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from .models import Project, Skill, Contact


def home(request):
    """Home page view."""
    try:
        # Check if table exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='portfolio_project'")
            table_exists = cursor.fetchone()
        
        if not table_exists:
            # Return page with empty data
            context = {
                'projects': [],
                'skills': [],
            }
            return render(request, 'portfolio/home.html', context)
        
        projects_list = list(Project.objects.all().order_by('-created_at')[:6])
        skills = list(Skill.objects.all())
        
        # Pre-process projects to split technologies
        for project in projects_list:
            if project.technologies:
                project.tech_list = [t.strip() for t in project.technologies.split(',')]
            else:
                project.tech_list = []
        
        context = {
            'projects': projects_list,
            'skills': skills,
        }
    except Exception:
        context = {
            'projects': [],
            'skills': [],
        }
    
    return render(request, 'portfolio/home.html', context)


def about(request):
    """About page view."""
    return render(request, 'portfolio/about.html')


def projects(request):
    """Projects page view."""
    try:
        # Check if table exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='portfolio_project'")
            table_exists = cursor.fetchone()
        
        if not table_exists:
            return render(request, 'portfolio/projects.html', {'projects': []})
        
        projects_list = list(Project.objects.all().order_by('-created_at'))
        
        # Pre-process projects to split technologies
        for project in projects_list:
            if project.technologies:
                project.tech_list = [t.strip() for t in project.technologies.split(',')]
            else:
                project.tech_list = []
        
        return render(request, 'portfolio/projects.html', {'projects': projects_list})
    except Exception:
        return render(request, 'portfolio/projects.html', {'projects': []})


def skills(request):
    """Skills page view."""
    try:
        # Check if table exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='portfolio_project'")
            table_exists = cursor.fetchone()
        
        if not table_exists:
            return render(request, 'portfolio/skills.html', {'skills_by_category': {}})
        
        skills = list(Skill.objects.all())
        # Group skills by category
        skills_by_category = {}
        for skill in skills:
            if skill.category not in skills_by_category:
                skills_by_category[skill.category] = []
            skills_by_category[skill.category].append(skill)
        return render(request, 'portfolio/skills.html', {'skills_by_category': skills_by_category})
    except Exception:
        return render(request, 'portfolio/skills.html', {'skills_by_category': {}})


def contact(request):
    """Contact page view."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')
        
        try:
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_text
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception:
            messages.error(request, 'Could not save message. Please try again.')
        
        return redirect('contact')
    
    return render(request, 'portfolio/contact.html')


def project_detail(request, project_id):
    """Project detail view."""
    try:
        project = Project.objects.get(id=project_id)
        # Pre-process technologies
        if project.technologies:
            project.tech_list = [t.strip() for t in project.technologies.split(',')]
        else:
            project.tech_list = []
        return render(request, 'portfolio/project_detail.html', {'project': project})
    except Project.DoesNotExist:
        return render(request, 'portfolio/404.html')
    except Exception:
        return render(request, 'portfolio/404.html')
