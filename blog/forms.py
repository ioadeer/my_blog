from django import forms
from blog.models import Category

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CreatePostForm(forms.Form):

    """ 
    This class is used to set  the create post form.
    """

    title = forms.CharField(max_length=100, help_text=_('Write the title here.'))
    text = forms.CharField(help_text=_('Write article here'),widget = forms.Textarea)
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())

from blog.models import Profile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'location', 'bio')

from blog.models import Comment
from pagedown.widgets import PagedownWidget

# comment form from https://github.com/drager/django-simple-blog

class UserCommentForm(forms.ModelForm):

    """
    This class is used to set the form of an authenticated user comment
    """

    error_msg = _(
            'Cannot be empty nor only contain spaces. Please fill in the field.')

    body_text = forms.CharField( widget = PagedownWidget() )

    class Meta:
        model = Comment
        fields = ["body_text"]
        
        """ 
        The following snippet sets a max length area extracted from the
        settings document. I choose no to use a configuration file.
        """
        #if MAX_LENGTH_TEXTAREA in not None:
        #    widgets = {
        #            'bodytext': forms.Textarea(attrs={'maxlegth': MAX_LENGTH_TEXTAREA})
        #    }

    def clean_bodytext(self):
        body_text = self.cleaned_data.get('body_text')
        if body_text:
            if not body_text.strip():
                raise forms.ValidationErro(self.error_msg)
        return body_text

class CommentForm(UserCommentForm):

    """
    This class is used to set the form of an unauthenticated user comment.
    """

    user_name = forms.CharField(label=_('Username'), initial=_('anonymous'))
    user_email = forms.EmailField(label=_('E-mail'), required=False)

    class Meta:
        model = Comment
        fields = ("user_name", "user_email", "body_text")
        #if MAX_LENGTH_TEXTAREA is not None:
        #    widgets = {
        #        'bodytext': forms.Textarea(attrs={'maxlength': MAX_LENGTH_TEXTAREA})
        #    }

    def clean_user_name(self):
        self.error_msg
        user_name = self.cleaned_data.get('user_name')
        if user_name:
            if not user_name.strip():
                raise forms.ValidationError(self.error_msg)
        return user_name
