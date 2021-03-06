from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from prismic_helper import PrismicHelper
from prismic import PREVIEW_COOKIE
import collections
#import logging

#logging.basicConfig(level=logging.DEBUG)

product_categories = {
    "Macaron": "Macarons",
    "Cupcake": "Cup Cakes",
    "Pie": "Little Pies"
}


def link_resolver(document):
    """
    Creates a local link to document.

    document_link -- Fragment.DocumentLink object
    """
    print "link_resolver"
    print document
    if document.get_document_type:
        if document.get_document_type() == "product":
            return reverse('prismic:product',
                           kwargs={'id': document.get_document_id(), 'slug': document.get_document_slug()})
        if document.get_document_type() == "blog-post":
            return reverse('prismic:blog_post',
                           kwargs={'id': document.get_document_id(), 'slug': document.get_document_slug()})
    return reverse('prismic:index')


def index(request):
    prismic = PrismicHelper(request)
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
    prismic = PrismicHelper(request)
    context = prismic.get_context()

    about_doc = prismic.get_bookmark("about")
    return render(request, 'prismic_app/about.html', {'context': context, 'about': about_doc})


def search(request):
    prismic = PrismicHelper(request)
    context = prismic.get_context()

    query = request.GET.get('query')
    if query is not None:
        products = prismic.form("everything")\
            .query("""[[:d = any(document.type, ["product", "selection"])][:d = fulltext(document, "{0}")]]""".format(query))\
            .ref(context["ref"]).submit()
        others = prismic.form("everything")\
            .query("""[[:d = any(document.type, ["article", "blog-post", "job-offer", "store"])][:d = fulltext(document, "{0}")]]""".format(query))\
            .ref(context["ref"]).submit()
    else:
        products = None
        others = None
        query = ""

    return render(request, 'prismic_app/search.html', {'context': context, 'products': products, 'others': others, 'query': query})


def selection(request):
    return HttpResponseNotFound


# -- Jobs


def jobs(request):
    prismic = PrismicHelper(request)
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
    prismic = PrismicHelper(request)
    context = prismic.get_context()

    return render(request, 'prismic_app/job_detail.html', {
        'context': context,
        'main': prismic.get_bookmark("jobs"),
        'job': prismic.get_document(id)
    })


# -- Products


PRODUCT_CATEGORIES = {
    "Macaron": "Macarons",
    "Cupcake": "Cup Cakes",
    "Pie": "Little Pies"
}


def products(request):
    prismic = PrismicHelper(request)
    context = prismic.get_context()

    all_products = sorted(prismic.form("products").ref(context["ref"]).submit().documents,
                          key=lambda p: p.get_text("product.name"))
    return render(request, 'prismic_app/products.html', {'context': context, 'products': all_products})


def product(request, id, slug):
    prismic = PrismicHelper(request)
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
    raise Http404


# -- Stores


WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def stores(request):
    prismic = PrismicHelper(request)
    context = prismic.get_context()

    all_stores = sorted(prismic.form("stores").ref(context["ref"]).submit().documents,
                          key=lambda p: p.get_text("store.name"))
    return render(request, 'prismic_app/stores.html', {
        'context': context,
        'main': prismic.get_bookmark("stores"),
        'stores': all_stores})


def store(request, id, slug):
    prismic = PrismicHelper(request)
    context = prismic.get_context()

    the_store = prismic.get_document(id)
    openings = map(lambda day: [day, the_store.get_text("store.%s[0]" % day.lower())], WEEKDAYS)
    return render(request, 'prismic_app/store_detail.html', {
        'context': context,
        'main': prismic.get_bookmark("stores"),
        'store': the_store,
        'openings': openings
        })


# -- Blog


BLOG_CATEGORIES = [
    "Announcements",
    "Do it yourself",
    "Behind the scenes"
]


def blog(request):
    prismic = PrismicHelper(request)
    context = prismic.get_context()

    category = request.GET.get('category')
    if category is not None:
        q = prismic.form("blog").query("""[[:d = at(my.blog-post.category, "%s")]]""" % category)
    else:
        q = prismic.form("blog")
    posts = list(sorted(q.ref(context["ref"]).submit().documents,
                        key=lambda post: post.get_date("blog-post.date")))[:10]
    return render(request, 'prismic_app/posts.html', {
        'context': context,
        'categories': BLOG_CATEGORIES,
        'posts': posts
    })


def blog_post(request, id, slug):
    prismic = PrismicHelper(request)
    context = prismic.get_context()

    post = prismic.get_document(id)
    related_posts = prismic.get_documents(map(lambda d: d.id, post.get_all("blog-post.relatedpost")))
    related_products = prismic.get_documents(map(lambda d: d.id, post.get_all("blog-post.relatedproduct")))

    return render(request, 'prismic_app/post_detail.html', {
        'context': context,
        'categories': BLOG_CATEGORIES,
        'post': post,
        'related_posts': related_posts,
        'related_products': related_products,
        'allow_comments': post.get_text("blog-post.allow_comments") == "Yes",
        'post_url': request.build_absolute_uri(reverse('prismic:blog_post', args=[post.id, post.slug]))
    })


# -- Previews


def preview(request):
    prismic = PrismicHelper(request)

    token = request.GET.get('token')

    if token is None:
        raise Http404

    url = prismic.api.preview_session(token, prismic.link_resolver, '/')
    print "url is = " + url

    response = redirect(url)
    response.set_cookie(PREVIEW_COOKIE, token, max_age=1800, httponly=False)
    return response