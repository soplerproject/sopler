# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from core.views import *

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/home')),
    url(r'^home$', ViewIndexPage.as_view(), name='ViewIndexPage'),
    url(r'^lists/AddList/$', AddList, name='AddList'),
    url(r'^lists/(?P<slug>[\w-]+)/$', ViewList.as_view(), name='list'),
    url(r'^lists/(?P<slug>[\w-]+)/AddNewItem/$', AddNewItem, name='AddNewItem'), 
    url(r'^lists/(?P<slug>[\w-]+)/AddNewComment/$', AddNewComment, name='AddNewComment'),
    url(r'^lists/(?P<slug>[\w-]+)/CheckItem/$', CheckItem, name='CheckItem'), 
    url(r'^lists/(?P<slug>[\w-]+)/UnCheckItem/$', UnCheckItem, name='UnCheckItem'), 
    url(r'^lists/(?P<slug>[\w-]+)/MarkItem/$', MarkItem, name='MarkItem'),
    url(r'^lists/(?P<slug>[\w-]+)/LockItem/$', LockItem, name='LockItem'),
    url(r'^lists/(?P<slug>[\w-]+)/DeleteItem/$', DeleteItem, name='DeleteItem'),
    url(r'^lists/(?P<slug>[\w-]+)/DeleteComment/$', DeleteComment, name='DeleteComment'),
    url(r'^lists/(?P<slug>[\w-]+)/DeleteList/$', DeleteList, name='DeleteList'),
    url(r'^lists/(?P<slug>[\w-]+)/DeletePreviousList/$', DeletePreviousList, name='DeletePreviousList'),
    url(r'^lists/(?P<slug>[\w-]+)/favit/$', favit, name='favit'),
    #
    # Disable Signup
    url(r'^accounts/signup/', RedirectView.as_view(url='/')),
)

