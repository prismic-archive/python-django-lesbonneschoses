from django.http import HttpResponse, Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from prismic_helper import PrismicHelper
import logging

logging.basicConfig(level=logging.DEBUG)


def link_resolver(document_link):
    """
    Creates a local link to document.

    document_link -- Fragment.DocumentLink object
    """

    # return reverse("prismic:document",args=document_link.id)
    return "/document/%s" % document_link.id

product_categories = {
    "Macaron": "Macarons",
    "Cupcake": "Cup Cakes",
    "Pie": "Little Pies"
}

def index(request):
    prismic = PrismicHelper()
    context = prismic.get_context()

    products = prismic.form("products").ref(context["ref"]).submit()
    featured = prismic.form("featured").ref(context["ref"]).submit()

    parameters = {
        'context': context, 'products': products, 'featured': featured,
        'product_categories': product_categories }
    return render(request, 'prismic_app/index.html', parameters)

def about(request):
    prismic = PrismicHelper()
    context = prismic.get_context()

    about_doc = prismic.get_bookmark("about")
    return render(request, 'prismic_app/about.html', {'context': context, 'about': about_doc} )

def products():
    pass