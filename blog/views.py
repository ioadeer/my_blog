from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category
# Create your views here.

def index(request):
   return render(request,'index.html')

from django.views import generic 
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

class PostListView(generic.ListView):
    model = Post
    paginate_by = 50

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

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'blog.delete_post'
    model = Post
    success_url = reverse_lazy('all-posts')

from blog.forms import CreatePostForm 
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse

from pdb import set_trace

@permission_required('blog.create_post')
def create_post(request):
    """ Create post view for authorized users """
    # no esta andando categories
    if request.method == "POST":
        form =  CreatePostForm(request.POST)
        if form.is_valid():
            #data = forms.cleaned_data
            data = {'title': form.cleaned_data['title']}
            user_name = request.user.username
            user = User.objects.filter(username__exact=user_name).first()
            data['author'] = user
            data['text'] = form.cleaned_data['text']
            post = Post.objects.create(**data)
            category_queryset = form.cleaned_data['categories']
            #print(category_queryset)
            post.categories.set(category_queryset)
            #set_trace()
            post.save()
            return HttpResponseRedirect(reverse('all-posts'))
    else:
        form = CreatePostForm()
        context = {
                'form' : form,
        }
        return render(request,'blog/create_post.html',context)


