# -*- coding: utf-8 -*-

import sys

from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime

from django.db.models.signals import post_syncdb
from django.contrib.sites.models import Site

from allauth.socialaccount.providers import registry
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.oauth.provider import OAuthProvider
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

# -------------
# List Model
# -------------
class List(models.Model):

    id   = models.AutoField(primary_key=True)
    slug = models.SlugField(unique=True, max_length=12)
    ListName = models.CharField(max_length=100)
    ListAuthOnly = models.BooleanField("Auth Only")
    ListPubDate = models.DateTimeField("Date List Published")
    
    ## List Owner Fields
    ListOwner = models.CharField("Owner's Handle",max_length=100)
    ListOwnerFN = models.CharField("Owner's First Name",max_length=100)
    ListOwnerLN = models.CharField("Owner's Last Name",max_length=100)
    ListOwnerState = models.CharField("Owner's Confirmation State",max_length=100)
    ListOwnerPrvdr = models.CharField("Owner's Provider",max_length=100)
    ListOwnerLink = models.CharField("Owner's Provider Link",max_length=150)
    ListIsPrivate = models.BooleanField("This list is Private")
    ListIsHidden = models.BooleanField("This list is Hidden")
    
    class Meta:
        ordering = ["ListOwner"]
        
        
    def __unicode__(self):
        return self.ListName

# -------------
# Item Model
# -------------
class Item(models.Model):

    list = models.ForeignKey('List') 
    content = models.TextField()
    
    ItemMarked = models.BooleanField()
    ItemLocked = models.BooleanField()
    ItemDueDate = models.DateField("Item Due Date",null=True)
    
    ## Item Done infos
    ItemDone = models.BooleanField()
    WhoDone =  models.CharField(max_length=150)
    TimeDone = models.DateTimeField("Date Completed")
    
    ## Item Owner Fields
    ItemOwner = models.CharField("Owner's Handle",max_length=100)
    ItemOwnerFN = models.CharField("Owner's First Name",max_length=100)
    ItemOwnerLN = models.CharField("Owner's Last Name",max_length=100)
    ItemOwnerState = models.CharField("Owner's Confirmation State",max_length=100)
    ItemOwnerPrvdr = models.CharField("Owner's Provider",max_length=100)
    ItemOwnerAvtr = models.CharField("Owner's Provider Avatar",max_length=150)
    ItemOwnerLink = models.CharField("Owner's Provider Link",max_length=150)

    class Meta:
        ordering = ["ItemOwner","ItemOwnerState","-ItemMarked","ItemDone"]

    def __unicode__(self):
        return self.content
        
        
# ---------------
# Comment Model
# ---------------
class Comment(models.Model):

    NewComment = models.ForeignKey(List)
    ComOwner = models.CharField("Owner's Handle",max_length=100)
    ComOwnerFN = models.CharField("Owner's First Name",max_length=100)
    ComOwnerState = models.CharField("Owner's Confirmation State",max_length=100)
    ComContent = models.TextField("Comment",max_length=100)
    ComPubDate = models.DateTimeField("Date Comment Published")


    def __unicode__(self):
        return self.ComContent


# ------------
# All-auth
# -----------
def setup_dummy_social_apps(sender, **kwargs):
    """
    `allauth` needs tokens for OAuth based providers. So let's
    setup some dummy tokens
    """
    site = Site.objects.get_current()
    for provider in registry.get_list():
        if (isinstance(provider, OAuth2Provider) 
            or isinstance(provider, OAuthProvider)):
            try:
                SocialApp.objects.get(provider=provider.id,
                                      sites=site)
            except SocialApp.DoesNotExist:
                print ("Installing dummy application credentials for %s."
                       " Authentication via this provider will not work"
                       " until you configure proper credentials via the"
                       " Django admin (`SocialApp` models)" % provider.id)
                app = SocialApp.objects.create(provider=provider.id,
                                               secret='secret',
                                               client_id='client-id',
                                               name='%s application' % provider.id)
                app.sites.add(site)


# We don't want to interfere with unittests et al
if 'syncdb' in sys.argv:
    post_syncdb.connect(setup_dummy_social_apps, sender=sys.modules[__name__])


