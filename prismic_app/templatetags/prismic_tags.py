from django import template
from prismic_app import views

register = template.Library()

context_name = "context"


@register.simple_tag(takes_context=True)
def link(context, object):
    return context[context_name]["link_resolver"](object)


@register.simple_tag(takes_context=True)
def as_html(context, object):
    return object.as_html(context[context_name]["link_resolver"])


@register.simple_tag(takes_context=True)
def get_html(context, object, field):
    return object.get_html(field, context[context_name]["link_resolver"])


@register.simple_tag
def get_text(document, field, default=""):
    value = document.get_text(field)
    return value if value is not None else default


@register.simple_tag
def get_number(document, field, format=None):
    number = document.get_number(field).value
    if format:
        return format % number
    else:
        return number


@register.simple_tag
def get_first_paragraph(document, field, default=""):
    stext = document.get_structured_text(field)
    return stext.get_first_paragraph().text if stext is not None else default


@register.simple_tag
def get_title(document, field, default=""):
    stext = document.get_structured_text(field)
    return stext.get_title().text if stext is not None else default


@register.simple_tag
def get_image(document, field, view="main", default="images/missing-image.png"):
    image = document.get_image(field, view)
    return image.url if image else default


@register.simple_tag
def excerpt(document, field, words=50):
    txt = document.get_text(field)
    if txt is None:
        return ""
    size = words * 10
    truncated = ' '.join(txt[:size].split(' ')[:-1])
    if truncated == txt:
        return truncated
    else:
        return truncated + "..."

