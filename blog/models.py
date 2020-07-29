from django.db import models
from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist

# method to name path of static image
# where profile is '/user_id/profile_picture/document_name
# and image from post is '/user_id/slug/document_name


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    slug = models.SlugField()
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')

    class Meta:
        ordering = ['created_on']
        permissions = (("create_post", "Can create post"), ("edit_post", "Can edit post"),)

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
    
    def to_dict(self):
        data = {
            'title' : self.title,
            'author': self.author.username,
            'first_name': self.author.first_name,
            'last_name': self.author.last_name,
            }
        return data


def create_slug(tempslug):
    slugcount = 0
    while True:
        try:
            Post.objects.get(slug=tempslug)
            slugcount += 1
            tempslug = tempslug + '-' + str(slugcount)
        except ObjectDoesNotExist:
            return tempslug

from django.contrib.auth.models import User

# adding profile picture media based on this tutorial
# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/etc
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length= 500, blank= True)
    location = models.CharField(max_length=30, blank= True)
    birth_date = models.DateField(null = True, blank = True)
    picture = models.FileField(upload_to=user_directory_path, blank = True)

    def get_absolute_url(self):
        return reverse('profile-detail', args=[str(self.id)])

#https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Comment(models.Model):
    post = models.ForeignKey( Post, on_delete=models.CASCADE )
    body_text = models.TextField( max_length= 500 )
    post_date = models.DateTimeField( auto_now_add=True )
    author = models.ForeignKey(
            settings.AUTH_USER_MODEL, null=True, blank=True,
            on_delete = models.SET_NULL)
    author_name = models.CharField(
            max_length=50, default='anonymous')
    author_email = models.EmailField(blank= True)

    def __str__(self):
        return self.body_text
