# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView, TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from core.api import ListResource

v1_api = Api(api_name='v1')
v1_api.register(ListResource())

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Examples:
    # url(r'^$', 'sopler.views.home', name='home'),
    url(r'^', include('core.urls', namespace="sopler")),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^login$', RedirectView.as_view(url='/lists/')),
    url(r'^accounts/profile/$', TemplateView.as_view(template_name='pages/profile.html')),
    url(r'^signin/$', TemplateView.as_view(template_name='socialaccount/signin.html')),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about/about.html')),
    url(r'^team/$', TemplateView.as_view(template_name='pages/about/team.html')),
    url(r'^terms/$', TemplateView.as_view(template_name='pages/about/terms.html')),
    url(r'^howto/$', TemplateView.as_view(template_name='pages/about/howto.html')),
    url(r'^privacy/$', TemplateView.as_view(template_name='pages/about/privacy.html')),
    # API
    url(r'^api/', include(v1_api.urls)),
)
