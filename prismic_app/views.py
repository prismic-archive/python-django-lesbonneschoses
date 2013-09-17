from django.http import HttpResponse, Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from prismic_shortcuts import Prismic_Helper
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
    prismic = Prismic_Helper()
    context = prismic.get_context()

    products_form = prismic.form("products")
    products_form.ref(context["ref"])
    products = products_form.submit()
    print products

    featured_form = prismic.form("featured")
    featured_form.ref(context["ref"])
    featured = products_form.submit()

    parameters = {
        'products': products, 'featured': featured, 'context': prismic.get_context(),
        'product_categories': product_categories }
    return render(request, 'prismic_app/index.html', parameters)


def detail(request, id, slug):
    prismic = Prismic_Helper()

    document = prismic.get_document(id)
    context = prismic.get_context()
    # context.link_resolver
    # print "context.link_resolver: %s" % context.link_resolver
    parameters = {'document': document, 'context': prismic.get_context()}
    return render(request, 'prismic_app/detail.html', parameters)

def products():
    pass