"""
Views for Portfolio Website
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone

from .models import (
    Project, Skill, Experience, Education, BlogPost, ContactMessage,
    Testimonial, Service, SocialLink, SiteInfo, VisitorCount, UserActivity
)
from .forms import (
    ContactForm, RegistrationForm, LoginForm, ProjectForm, SkillForm,
    ExperienceForm, EducationForm, BlogPostForm, TestimonialForm,
    ServiceForm, SocialLinkForm
)


# ==================== Public Views ====================

class HomeView(TemplateView):
    """
    Home page view with hero section and overview
    """
    template_name = 'portfolio/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get site info
        from portfolio.models import SiteInfo
        context['site_info'] = SiteInfo.objects.first()
        
        # Get featured projects
        context['featured_projects'] = Project.objects.filter(
            is_published=True, 
            featured=True
        ).order_by('-created_at')[:6]
        
        # Get skills grouped by category
        skills = Skill.objects.filter(is_active=True).order_by('-proficiency')
        context['skills'] = skills
        context['backend_skills'] = skills.filter(category='backend')
        context['frontend_skills'] = skills.filter(category='frontend')
        context['database_skills'] = skills.filter(category='database')
        context['tools_skills'] = skills.filter(category='tools')
        
        # Get services
        context['services'] = Service.objects.filter(is_active=True).order_by('order')
        
        # Get testimonials
        context['testimonials'] = Testimonial.objects.filter(
            is_active=True
        ).order_by('-order', '-created_at')[:5]
        
        # Get experience
        context['experiences'] = Experience.objects.order_by('-start_date')[:3]
        
        return context


class AboutView(TemplateView):
    """
    About page with biography and experience
    """
    template_name = 'portfolio/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get site info
        from portfolio.models import SiteInfo
        context['site_info'] = SiteInfo.objects.first()
        
        # Get all experiences
        context['experiences'] = Experience.objects.order_by('-start_date')
        
        # Get all education
        context['educations'] = Education.objects.order_by('-start_date')
        
        # Get site info
        context['site_info'] = SiteInfo.objects.first()
        
        return context


class ProjectsView(ListView):
    """
    Portfolio projects listing page
    """
    model = Project
    template_name = 'portfolio/projects.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        return Project.objects.filter(
            is_published=True
        ).order_by('-featured', '-created_at')


class ProjectDetailView(DetailView):
    """
    Single project detail page
    """
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        return Project.objects.filter(is_published=True)
    
    def get_context_data(self, **context):
        context = super().get_context_data(**context)
        context['related_projects'] = Project.objects.filter(
            is_published=True
        ).exclude(pk=self.object.pk)[:3]
        return context


class SkillsView(TemplateView):
    """
    Skills and expertise page
    """
    template_name = 'portfolio/skills.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all skills grouped by category
        skills = Skill.objects.filter(is_active=True).order_by('-proficiency')
        context['all_skills'] = skills
        context['backend_skills'] = skills.filter(category='backend')
        context['frontend_skills'] = skills.filter(category='frontend')
        context['database_skills'] = skills.filter(category='database')
        context['tools_skills'] = skills.filter(category='tools')
        
        return context


class BlogView(ListView):
    """
    Blog listing page
    """
    model = BlogPost
    template_name = 'portfolio/blog.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        return BlogPost.objects.filter(
            is_published=True
        ).order_by('-published_at')


class BlogDetailView(DetailView):
    """
    Single blog post detail page
    """
    model = BlogPost
    template_name = 'portfolio/blog_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)
    
    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        # Increment views
        post.views += 1
        post.save()
        return post
    
    def get_context_data(self, **context):
        context = super().get_context_data(**context)
        context['related_posts'] = BlogPost.objects.filter(
            is_published=True,
            category=self.object.category
        ).exclude(pk=self.object.pk)[:3]
        return context


class ContactView(TemplateView):
    """
    Contact page with form
    """
    template_name = 'portfolio/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                'Thank you for contacting me! I will get back to you soon.',
                extra_tags='alert-success'
            )
            return redirect('portfolio:contact')
        
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)


class ServicesView(TemplateView):
    """
    Services page
    """
    template_name = 'portfolio/services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(
            is_active=True
        ).order_by('order')
        return context


# ==================== Authentication Views ====================

def register_view(request):
    """
    User registration view
    """
    if request.user.is_authenticated:
        return redirect('portfolio:dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, 
                f'Welcome {user.username}! Your account has been created successfully.',
                extra_tags='alert-success'
            )
            return redirect('portfolio:dashboard')
    else:
        form = RegistrationForm()
    
    return render(request, 'portfolio/register.html', {'form': form})


def login_view(request):
    """
    User login view
    """
    if request.user.is_authenticated:
        return redirect('portfolio:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Log activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='login',
                    description=f'User logged in'
                )
                
                messages.success(
                    request, 
                    f'Welcome back, {username}!',
                    extra_tags='alert-success'
                )
                
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('portfolio:dashboard')
            else:
                messages.error(
                    request, 
                    'Invalid username or password.',
                    extra_tags='alert-danger'
                )
        else:
            messages.error(
                request, 
                'Invalid username or password.',
                extra_tags='alert-danger'
            )
    else:
        form = LoginForm()
    
    return render(request, 'portfolio/login.html', {'form': form})


def logout_view(request):
    """
    User logout view
    """
    if request.user.is_authenticated:
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            activity_type='logout',
            description=f'User logged out'
        )
        
        logout(request)
        messages.success(
            request, 
            'You have been logged out successfully.',
            extra_tags='alert-info'
        )
    
    return redirect('portfolio:home')


# ==================== Dashboard Views ====================

@login_required
def dashboard_view(request):
    """
    User dashboard view
    """
    # Get user's recent activities
    recent_activities = UserActivity.objects.filter(
        user=request.user
    )[:10]
    
    # Get statistics
    total_projects = Project.objects.count()
    published_projects = Project.objects.filter(is_published=True).count()
    total_skills = Skill.objects.filter(is_active=True).count()
    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    
    context = {
        'recent_activities': recent_activities,
        'total_projects': total_projects,
        'published_projects': published_projects,
        'total_skills': total_skills,
        'total_messages': total_messages,
        'unread_messages': unread_messages,
    }
    
    return render(request, 'portfolio/dashboard.html', context)


@login_required
def profile_view(request):
    """
    User profile view
    """
    # Get or create site info for profile image
    from portfolio.models import SiteInfo
    site_info = SiteInfo.objects.first()
    
    if request.method == 'POST':
        # Update user profile
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        # Update site info email as well
        if site_info:
            site_info.email = request.POST.get('email', '')
            site_info.save()
        else:
            SiteInfo.objects.create(email=request.POST.get('email', ''))
        
        # Handle profile image upload
        if 'profile_image' in request.FILES:
            if site_info:
                site_info.profile_image = request.FILES['profile_image']
                site_info.save()
            else:
                SiteInfo.objects.create(profile_image=request.FILES['profile_image'])
        
        messages.success(
            request, 
            'Profile updated successfully!',
            extra_tags='alert-success'
        )
        return redirect('portfolio:profile')
    
    return render(request, 'portfolio/profile.html', {'user': request.user, 'site_info': site_info})


@login_required
def messages_view(request):
    """
    View all contact messages
    """
    messages_list = ContactMessage.objects.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(messages_list, 10)
    page = request.GET.get('page')
    
    try:
        messages_page = paginator.page(page)
    except PageNotAnInteger:
        messages_page = paginator.page(1)
    except EmptyPage:
        messages_page = paginator.page(paginator.num_pages)
    
    return render(request, 'portfolio/messages.html', {'messages': messages_page})


@login_required
def mark_message_read(request, pk):
    """
    Mark a contact message as read
    """
    message = get_object_or_404(ContactMessage, pk=pk)
    message.is_read = True
    message.save()
    
    messages.success(request, 'Message marked as read.')
    return redirect('portfolio:messages')


# ==================== API Views ====================

def api_skills(request):
    """
    API endpoint to get all skills
    """
    skills = Skill.objects.filter(is_active=True).order_by('-proficiency')
    data = [
        {
            'id': skill.id,
            'name': skill.name,
            'category': skill.category,
            'proficiency': skill.proficiency,
            'icon_class': skill.icon_class,
        }
        for skill in skills
    ]
    return JsonResponse(data, safe=False)


def api_projects(request):
    """
    API endpoint to get all published projects
    """
    projects = Project.objects.filter(is_published=True).order_by('-created_at')
    data = [
        {
            'id': project.id,
            'title': project.title,
            'slug': project.slug,
            'short_description': project.short_description,
            'image': project.image.url if project.image else None,
            'project_url': project.project_url,
            'source_code_url': project.source_code_url,
            'technology_used': project.get_technology_list(),
        }
        for project in projects
    ]
    return JsonResponse(data, safe=False)


def api_contact(request):
    """
    API endpoint to submit contact form
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Message sent successfully!'})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
