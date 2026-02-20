"""
Admin Configuration for Portfolio Website
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteInfo, SocialLink, Skill, Project, Experience, Education,
    BlogPost, ContactMessage, VisitorCount, UserActivity, Testimonial, Service
)


@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'owner_name', 'email', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_title', 'site_description', 'owner_name')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Files', {
            'fields': ('profile_image', 'resume')
        }),
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'is_active', 'order']
    list_filter = ['is_active', 'platform']
    list_editable = ['is_active', 'order']
    search_fields = ['platform', 'url']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency', 'is_active', 'order']
    list_filter = ['category', 'is_active']
    list_editable = ['is_active', 'order', 'proficiency']
    search_fields = ['name', 'category']
    ordering = ['-proficiency', 'name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'is_published', 'order', 'created_at']
    list_filter = ['is_published', 'featured']
    list_editable = ['is_published', 'featured', 'order']
    search_fields = ['title', 'description', 'technology_used']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('Images', {
            'fields': ('image',)
        }),
        ('Links', {
            'fields': ('project_url', 'source_code_url')
        }),
        ('Details', {
            'fields': ('technology_used', 'featured', 'is_published', 'order')
        }),
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company_name', 'start_date', 'end_date', 'is_current', 'order']
    list_filter = ['is_current']
    list_editable = ['is_current', 'order']
    search_fields = ['position', 'company_name']
    ordering = ['-start_date']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'field_of_study', 'institution', 'start_date', 'end_date', 'order']
    list_editable = ['order']
    search_fields = ['degree', 'field_of_study', 'institution']
    ordering = ['-start_date']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'is_featured', 'views', 'published_at']
    list_filter = ['is_published', 'is_featured', 'category']
    list_editable = ['is_published', 'is_featured']
    search_fields = ['title', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-published_at']
    date_hierarchy = 'published_at'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'is_replied', 'created_at']
    list_filter = ['is_read', 'is_replied']
    list_editable = ['is_read', 'is_replied']
    search_fields = ['name', 'email', 'subject', 'message']
    ordering = ['-created_at']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']


@admin.register(VisitorCount)
class VisitorCountAdmin(admin.ModelAdmin):
    list_display = ['count', 'last_visitor']
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not VisitorCount.objects.exists()


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'description', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__username', 'description']
    ordering = ['-created_at']
    readonly_fields = ['user', 'activity_type', 'description', 'ip_address', 'user_agent', 'created_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_title', 'rating', 'is_active', 'order']
    list_filter = ['is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['client_name', 'testimonial']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon_class', 'is_active', 'order']
    list_filter = ['is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
