from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts', views.PostListView.as_view(), name='all-posts'),
    path('posts/<slug:slug>', views.view_post, name='post-detail'),
    path('post/create/', views.PostCreate.as_view(), name='post-create'),
    path('post/<slug:slug>/update', views.PostUpdate.as_view(), name='post-update'),
    path('post/<slug:slug>/delete', views.PostDelete.as_view(), name='post-delete'),
    path('post/create_post/', views.create_post, name='create-post')
]


