from django.shortcuts import render
from django.core.urlresolvers import reverse
from prismic_helper import PrismicHelper
import collections
#import logging

#logging.basicConfig(level=logging.DEBUG)

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
    return reverse('prismic:product',
                   kwargs={'id': document_link.get_document_id(), 'slug': document_link.get_document_slug()})


def index(request):
    prismic = PrismicHelper()
    context = prismic.get_context()

    products = prismic.form("products").ref(context["ref"]).submit().documents
    featured = prismic.form("featured").ref(context["ref"]).submit().documents

    parameters = {
        'context': context,
        'products': products,
        'featured': featured,
        'product_categories': product_categories
    }
    return render(request, 'prismic_app/index.html', parameters)


def about(request):
    prismic = PrismicHelper()
    context = prismic.get_context()

    about_doc = prismic.get_bookmark("about")
    return render(request, 'prismic_app/about.html', {'context': context, 'about': about_doc})


def jobs(request):
    prismic = PrismicHelper()
    context = prismic.get_context()

    jobs_doc = prismic.get_bookmark("jobs")
    services = collections.OrderedDict()
    services["Store"] = []
    services["Office"] = []
    services["Workshop"] = []
    services["Other"] = []
    for j in prismic.form("jobs").ref(context["ref"]).submit().documents:
        service = j.get_text("job-offer.service")
        if service in services:
            services[service].append(j)
        else:
            services["Other"].append(j)
    return render(request, 'prismic_app/jobs.html', {'context': context, 'jobs': jobs_doc, 'services': services})


def job(request, id, slug):
    pass


def products(request):
    prismic = PrismicHelper()
    context = prismic.get_context()

    all_products = sorted(prismic.form("products").ref(context["ref"]).submit().documents,
                          key=lambda p: p.get_text("product.name"))
    return render(request, 'prismic_app/products.html', {'context': context, 'products': all_products})


def product(request, id, slug):
    prismic = PrismicHelper()
    context = prismic.get_context()

    product = prismic.get_document(id)
    summary = product.get_text('product.short_lede')
    if summary is None:
        summary = product.get_text('product.name')

    related = prismic.get_documents(map(lambda d: d.id, product.get_all("product.related")))

    return render(request, 'prismic_app/product_detail.html', {
        'context': context,
        'product': product,
        'summary': summary,
        'author': product.get_text("product.testimonial_author"),
        'quote': product.get_text("product.testimonial_quote"),
        'related': related
    })


def products_by_flavour(request):
    pass
