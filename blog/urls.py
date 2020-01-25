from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts', views.PostListView.as_view(), name='all-posts'),
    path('posts/<slug:slug>', views.view_post, name='post-detail'),
    path('post/create/', views.PostCreate.as_view(), name='post-create'),
    path('post/<slug:slug>/update', views.PostUpdate.as_view(), name='post-update'),
    path('post/<slug:slug>/delete', views.PostDelete.as_view(), name='post-delete'),
    path('post/create_post/', views.create_post, name='create-post'),
    path('post/search/', views.search, name='search-post'),
    path('profile_update', views.update_profile,name='profile-update'),
    #path('profile/create/', views.ProfileCreate.as_view(), name='profile-create')
]

urlpatterns += [
    path('profiles', views.ProfileListView.as_view(), name='all-profiles'),
    #path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='profile-detail')
    path('profile/<int:pk>', views.ProfileDetailView, name='profile-detail')
    ]

urlpatterns += [
    path('ajax/search/', views.autocomplete, name='auto-complete')
    ]
