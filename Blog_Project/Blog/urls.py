from django.urls import path
from Blog.views import (
    home,
    edit_post, delete_post,
    edit_category, delete_category,
    edit_comment, delete_comment,
)

urlpatterns = [
    path('', home, name='home'),
    path('post/edit/<int:pk>/', edit_post, name='edit_post'),
    path('post/delete/<int:pk>/', delete_post, name='delete_post'),
    path('category/edit/<int:pk>/', edit_category, name='edit_category'),
    path('category/delete/<int:pk>/', delete_category, name='delete_category'),
    path('comment/edit/<int:pk>/', edit_comment, name='edit_comment'),
    path('comment/delete/<int:pk>/', delete_comment, name='delete_comment'),
]
