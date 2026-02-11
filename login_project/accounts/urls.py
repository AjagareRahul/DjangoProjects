from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),# FIRST PAGE
    path('login/', views.login_view, name='login'),      
    path('logout/', views.logout_view, name='logout'),


    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('add_items/',views.add_items,name='add_item'),
    path('contact/', views.contact, name='contact'),

    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    #path('cement-list/',views.cement_list,name='cement_list'),
    path('add-cement/',views.add_cement,name='cement'),
    path('cement-verity/', views.cement_verity, name='cement_verity'),

]
