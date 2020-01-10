from django.test import TestCase

from blog.models import Post, Category
from django.contrib.auth.models import User

class PostModelTestClass(TestCase):
#class AnotherTest( TestCase ):

    @classmethod
    def setUpTestData(cls):
        # Creating various post with same title 
        author = User.objects.create(username="test_user")
        test_category_1 = Category.objects.create(name="Science")
        test_category_2 = Category.objects.create(name="Gastronomy")
        categories = [test_category_1, test_category_2]
        post = Post.objects.create(author = author, title="title")
        post.categories.set(categories)
        post.save()
        posts = 5 
        for idx in range(posts):
            post = Post.objects.create(author = author,title="title")
            post.save()

        # Creat single Post
 
    def setUp(self):
        pass

    def test_string_method_returns_title(self):
        post = Post.objects.get(id=1)
        self.assertEquals("title", post.__str__())

    def test_slug_creation_method(self):

        """ Test creation method which appends a number at the end of the slug
        when there is already an equally named slug. It is not a good method to
        create new slugs, but it is better than nothing. I copied it from the
        internet"""

        slug = "title"
        for i in range(1,6,1):
            post = Post.objects.get(id=i+1)
            slug += "-"+str(i)
            self.assertEquals(slug,post.slug) 
