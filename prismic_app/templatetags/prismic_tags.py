from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def as_html(object, context):
    return object.as_html(context["link_resolver"])

@register.simple_tag
def get_html(object, field, context):
    return object.get_html(field, context["link_resolver"])

@register.simple_tag
def get_text(document, field):
    return document.get_text(field)

@register.simple_tag
def get_number(document, field, format=None):
    number = document.get_number(field).value
    if format:
        return format % number
    else:
        return number

@register.simple_tag
def get_image(document, field, view="main"):
    image = document.get_image(field, view)
    return image.url if image else None