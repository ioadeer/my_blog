from django.shortcuts import render, get_object_or_404
from blog.models import Post
# Create your views here.

def index(request):
   return render(request,'index.html')

from django.views import generic 

class PostListView(generic.ListView):
    model = Post
    paginate_by = 10

#class PostDetailView(generic.DetailView):
#    model = Post

def view_post(request, slug):
    context = {'post': get_object_or_404(Post, slug=slug)}
    return render(request, 'blog/post_detail.html',context)
