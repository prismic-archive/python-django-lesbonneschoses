from django.conf.urls import patterns, url

from prismic_app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^product/(?P<id>[-_a-zA-Z0-9]{16})/(?P<slug>.*)', views.products, name='product'),
    url(r'^products/', views.products, name='products'),
    url(r'^about/', views.about, name='about'),
)
