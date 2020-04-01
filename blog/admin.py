from django.contrib import admin
from .models import Post, Category, Profile, Comment
# Register your models here.

#admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'text')
    fields = [('title','author'), 'text', 'categories']

#admin.site.register(Category)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name','post_date','body_text',)
    fields = [('author_name', 'post'), 'body_text']
