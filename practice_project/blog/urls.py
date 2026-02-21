from django.urls import path
from blog import views
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:id>/', views.post_details, name='post_details'),
    path('create/',views.create_post,name='create_post'),
    path('update/<int:id>/',views.update_post,name='update_post'),
    path('delete/<int:id>/',views.delete_post,name='delete_post'),
]
