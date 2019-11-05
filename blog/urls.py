from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts', views.PostListView.as_view(), name='all-posts'),
    path('posts/<slug:slug>', views.view_post, name='post-detail'),
]
