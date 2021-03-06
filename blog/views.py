from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category, Comment
# Create your views here.

from pdb import set_trace

def index(request):
    #set_trace()
    posts = Post.objects.all().order_by( '-created_on' )[:5]
    profiles = Profile.objects.all()[:3]
    context ={
            'posts': posts,
            'profiles': profiles,
            }
    return render(request,'index.html', context)

from django.views import generic 
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

class PostListView(generic.ListView):
    model = Post
    paginate_by = 10


from blog.forms import UserCommentForm, CommentForm 

class PostDetailView(generic.DetailView):
    model = Post
    page_template = "blog/post_detail.html"

def view_post(request, slug):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = UserCommentForm( request.POST )
        else:
            form = CommentForm( request.POST )
        if form.is_valid():
            data = { 'body_text': form.cleaned_data[ 'body_text' ] }
            post = get_object_or_404( Post, slug=slug )
            data[ 'post' ]  = post
            if request.user.is_authenticated:
                data[ 'author' ] = request.user
                data[ 'author_name' ] = request.user.username
                data[ 'author_email' ] = request.user.email
            comment = Comment.objects.create( **data )
            comment.save()
            return redirect( post.get_absolute_url() )
    else:
        if request.user.is_authenticated:
            form = UserCommentForm()
        else:
            form = CommentForm()
        # aca falta agregar comments a context
        post = get_object_or_404( Post, slug=slug )
        comments = Comment.objects.filter(post=post)
        context = {
                'post': get_object_or_404( Post, slug=slug),
                'comment_form': form,
                'comments' : comments,
                }
        return render(request, 'blog/post_detail.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView

class PostCreate(CreateView):
    model = Post
    fields = ['author', 'title', 'text', 'categories'] 

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'text', 'categories']
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):

        context = super().get_context_data( **kwargs )
        if( self.request.user.username == context[ "post" ].author.username ):
            return context
        else:
            raise PermissionDenied

class PostDelete(PermissionRequiredMixin, DeleteView):

    permission_required = 'blog.delete_post'
    model = Post
    success_url = reverse_lazy( 'all-posts' )

from blog.forms import CreatePostForm 
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse


@permission_required('blog.create_post')
def create_post(request):
    """ Create post view for authorized users """
    # no esta andando categories
    if request.method == "POST":
        form =  CreatePostForm(request.POST)
        if form.is_valid():
            data = { 'title': form.cleaned_data[ 'title' ]}
            user_name = request.user.username
            user = User.objects.filter( username__exact=user_name ).first()
            data[ 'author' ] = user
            data[ 'text' ] = form.cleaned_data[ 'text' ]
            post = Post.objects.create( **data )
            category_queryset = form.cleaned_data[ 'categories' ]
            post.categories.set( category_queryset )
            post.save()
            return HttpResponseRedirect( reverse( 'all-posts' ))
    else:
        form = CreatePostForm()
        context = {
                'form' : form,
        }
        return render(request,'blog/create_post.html',context)

from django.db.models import Q
def search(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
                Q( title__icontains= query ) |
                Q( author__username__icontains= query ) |
                Q( text__icontains= query ) |
                Q( categories__name__icontains= query )
        )
        results = Post.objects.filter( qset ).distinct()

    else:
        results = []

    return render(request, 'blog/search.html', {
        "results" : results,
        "query" : query,
        })

from blog.models import Profile
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.db import transaction
from blog.forms import UserForm, ProfileForm
from django.shortcuts import redirect

# de aca https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance = request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance= request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            #return redirect('settings:profile')
            return HttpResponseRedirect(reverse('profile-detail', args=[str(request.user.profile.id)]))
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'blog/profile_update.html',{
        'user_form': user_form,
        'profile_form': profile_form,
        })

class ProfileListView(generic.ListView):
    model = Profile 

#class ProfileDetailView(generic.DetailView):
#    model = Profile

def ProfileDetailView(request, pk):
    profile = get_object_or_404(Profile, pk = pk)
    posts = Post.objects.filter( author__exact=profile.user ).order_by( 'created_on' )[:5]
    context = {
            'profile': profile, 
            'posts' : posts,
            }
    return render( request, 'blog/profile_detail.html', context)

import json
from django.http import JsonResponse
from django.core import serializers

def autocomplete(request):

    if request.method == 'GET':
        query = request.GET.get( 'q' , '')
        if query:
            qset = (
                    Q( title__istartswith=query ) |
                    Q( author__username__istartswith=query )
            )
            results = Post.objects.filter( qset ).distinct()
            results_as_dict_array = [ result.to_dict() for result in results ]
            data = json.dumps( results_as_dict_array )
        else:
            data = { 'data': 'fail' }
    else:
        data = { 'data' : 'fail' }

    return JsonResponse( data, safe=False )
