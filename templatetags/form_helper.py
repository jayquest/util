from django.forms.fields import Field

__author__ = 'Johnny'


from django import template
from django import forms
register = template.Library()

@register.filter
def field_is_required(field):
    try:
        return field.field.required
    except AttributeError:
        return False

@register.filter
def field_widget(field):
    if isinstance(field,Field):
        return field.widget.__class__.__name__
    else:
        return field.field.widget.__class__.__name__

