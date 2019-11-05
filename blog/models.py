from django.db import models
from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    slug = models.SlugField()
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')

    def save(self, *args, **kwargs):
        tempslug = slugify(self.title)
        if self.id:
            blogpost = Post.objects.get(pk=self.id)
            if blogpost.title != self.title:
                self.slug = create_slug(tempslug)
        else:
            self.slug = create_slug(tempslug)

        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',args=[self.slug])

def create_slug(tempslug):
    slugcount = 0
    while True:
        try:
            Post.objects.get(slug=tempslug)
            slugcount += 1
            tempslug = tempslug + '-' + str(slugcount)
        except ObjectDoesNotExist:
            return tempslug
