from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def as_html(object, prismic_context):
    return mark_safe(object.as_html(prismic_context["link_resolver"]))

@register.simple_tag
def pget_text(document, field):
    return document.get_text(field)

@register.simple_tag
def pget_number(document, field, format=None):
    number = document.get_number(field).value
    if format:
        return format % number
    else:
        return number

@register.simple_tag
def pget_image(document, field, view="main"):
    image = document.get_image(field, view)
    return image.url if image else None