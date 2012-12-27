__author__ = 'Johnny'

from django import template

register = template.Library()

@register.simple_tag
def current_page(request, pattern, css_class = None):
    if(css_class == None):
        css_class = 'current'

    import re
    if(pattern == '/'):
        if(pattern == request.path):
            return css_class
    else:
        if re.search(pattern, request.path):
            return css_class
    return ''
