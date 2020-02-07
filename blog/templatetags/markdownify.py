from django import template
import mistune

"""
https://www.ignoredbydinosaurs.com/posts/275-easy-markdown-and-syntax-highlighting-django
agregando filtro para parsear markdown
"""

register = template.Library()

@register.filter
def markdown(value):
    markdown = mistune.Markdown()
    return markdown(value)
