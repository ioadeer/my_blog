from django.shortcuts import render, get_object_or_404
from blog.models import Post
# Create your views here.

def index(request):
   return render(request,'index.html')

from django.views import generic 

class PostListView(generic.ListView):
    model = Post
    paginate_by = 10

class PostDetailView(generic.DetailView):
    model = Post

def view_post(request, slug):
    context = {'post': get_object_or_404(Post, slug=slug)}
    return render(request, 'blog/post_detail.html',context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
class PostCreate(CreateView):
    model = Post
    fields = ['author', 'title', 'text', 'categories',] 

class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'text', 'categories']

from blog.forms import CreatePostForm 
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse

@permission_required('blog.create_post')
def create_post(request):
    """ Create post view for authorized users """
    if request.method == "POST":
        form =  CreatePostForm(request.POST)
        if form.is_valid():
            #data = forms.cleaned_data
            data = {'title': form.cleaned_data['title']}
            print(data)
            data['author'] = request.user
            print(data)
            post = Post.objects.create(**data)
            post.save()
            return HttpResponseRedirect(reverse('all-posts'))
    else:
        form = CreatePostForm()
        context = {
                'form' : form,
        }
        return render(request,'blog/create_post.html',context)


