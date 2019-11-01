from django.contrib import admin
from .models import Post
# Register your models here.

#admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'text')
    fields = [('title','author'), 'text']# 'categories']
