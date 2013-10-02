from django.shortcuts import render
from django.core.urlresolvers import reverse
from prismic_helper import PrismicHelper

product_categories = {
    "Macaron": "Macarons",
    "Cupcake": "Cup Cakes",
    "Pie": "Little Pies"
}


def link_resolver(document_link):
    """
    Creates a local link to document.

    document_link -- Fragment.DocumentLink object
    """
    return reverse('prismic:product', kwargs={'id': document_link.get_document_id(), 'slug': document_link.get_document_slug()})


def index(request):
    prismic = PrismicHelper()
    context = prismic.get_context()

    products = prismic.form("products").ref(context["ref"]).submit()
    featured = prismic.form("featured").ref(context["ref"]).submit()

    parameters = {
        'context': context, 'products': products, 'featured': featured, 'product_categories': product_categories
    }
    return render(request, 'prismic_app/index.html', parameters)


def about(request):
    prismic = PrismicHelper()
    context = prismic.get_context()

    about_doc = prismic.get_bookmark("about")
    return render(request, 'prismic_app/about.html', {'context': context, 'about': about_doc})


def products(request):
    pass
