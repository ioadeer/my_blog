from django import forms
from blog.models import Category

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class CreatePostForm(forms.Form):
    title = forms.CharField(max_length=100, help_text="Write the title here.")
    text = forms.CharField(help_text="Write article here",widget = forms.Textarea)
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
