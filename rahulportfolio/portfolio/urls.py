"""
URL Configuration for Portfolio Application
"""

from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Public pages
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('skills/', views.SkillsView.as_view(), name='skills'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('services/', views.ServicesView.as_view(), name='services'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard (requires login)
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('messages/', views.messages_view, name='messages'),
    path('messages/<int:pk>/read/', views.mark_message_read, name='mark_message_read'),
    
    # API endpoints
    path('api/skills/', views.api_skills, name='api_skills'),
    path('api/projects/', views.api_projects, name='api_projects'),
    path('api/contact/', views.api_contact, name='api_contact'),
]
