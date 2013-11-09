# -*- coding: utf-8 -*-

import hashlib
import time
import random
import re

from django.utils import timezone
from django.views.generic import DetailView, TemplateView, ListView
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

# Sopler Models
from core.models import List, Item, Comment

# Allauth Models
import allauth.socialaccount.models


pages_dir = "pages/"


class ViewIndexPage(ListView):
    model = List
    template_name = pages_dir + "index.html"
	

class ViewProfilePage(TemplateView):
    template_name = pages_dir + "profile.html"


class ViewList(DetailView):
    model = List
    template_name = pages_dir + "sidepanel.html"
    
    def get_context_data(self, **kwargs):
      context = super(ViewList, self).get_context_data(**kwargs)
      context['lists'] = List.objects.all()
      return context

#################################################
# Create A New List
#################################################

def AddList(request):

    if request.user.is_anonymous():
    	ListOwner = request.POST.get('ListOwnerName')
        ListOwnerFN = ""
        ListOwnerLN = ""
        ListOwnerState = "non-confirmed"
        ListOwnerPrvdr = ""
        ListOwnerLink = ""

    else:
        for account in request.user.socialaccount_set.all():
          ListOwnerPrvdr = account.provider

          if ListOwnerPrvdr == "facebook": 
	    	  ListOwner   = account.extra_data['username']
                  ListOwnerFN = account.extra_data['first_name']
                  ListOwnerLN = account.extra_data['last_name']
		  ListOwnerState = "confirmed"
		  ListOwnerLink = account.extra_data['link']

	  elif ListOwnerPrvdr == "twitter":
	    	  ListOwner   = account.extra_data['screen_name']
                  ListOwnerFN = account.extra_data['name']
                  ListOwnerLN = ""
		  ListOwnerState = "confirmed"
		  ListOwnerLink = "https://twitter.com/" + account.extra_data['screen_name']
		  
	  elif ListOwnerPrvdr == "google":
	    	  ListOwner   = account.extra_data['name'] 
                  ListOwnerFN = account.extra_data['id']
                  ListOwnerLN = ""
		  ListOwnerState = "confirmed"
		  ListOwnerLink = account.extra_data['link'] 
		  
	  elif ListOwnerPrvdr == "persona":
	    	  ListOwner   = account.user
                  ListOwnerFN = ""
                  ListOwnerLN = ""
		  ListOwnerState = "confirmed"
		  ListOwnerLink = "" 
	  else:
	  	  pass

    req = request.POST['ListName'].encode('utf-8')
    ListAuthOnly = request.POST.get('ListAuthOnly')

    if ListAuthOnly: 
        ListAuthOnly = True
    else:
        ListAuthOnly = False

    now = time.time()
    sha256 = hashlib.sha256()
    sha256.update(req)
    ParamAlpha = sha256.hexdigest()

    sha256.update(str(now))
    ParamBeta = sha256.hexdigest()

    sha256.update(ParamAlpha + ParamBeta)
    CryptLink = sha256.hexdigest()

    random.choice(CryptLink)
    CryptLink = ''.join(random.sample(CryptLink,12))

    p = List(
	ListName = req,
	slug = slugify(CryptLink), 
	ListAuthOnly = ListAuthOnly, 
	ListOwner = ListOwner, 
        ListOwnerFN = ListOwnerFN,  
        ListOwnerLN = ListOwnerLN,
	ListOwnerState = ListOwnerState,
	ListOwnerPrvdr = ListOwnerPrvdr, 
	ListOwnerLink = ListOwnerLink, 
	ListPubDate = timezone.now()
	)

    p.save()

    list = get_object_or_404(List, slug=slugify(CryptLink))
    return HttpResponseRedirect('/lists/' + list.slug)
  
  
#################################################
# Delete List
#################################################

def DeleteList(request, slug):
    list = get_object_or_404(List, slug=slug)
    p = get_object_or_404(List, pk=int(request.POST['list_pk']))
    p.delete()
    
    return HttpResponseRedirect('/lists/')


#################################################
# Delete Previous Lists
#################################################

def DeletePreviousList(request, slug):
    list = get_object_or_404(List, slug=slug)
    p = get_object_or_404(List, pk=int(request.POST['list_pk']))
    p.delete()
    
    return HttpResponseRedirect('/')


#################################################
# Add A New Comment
#################################################

def AddNewComment(request, slug):
    if request.user.is_anonymous():
    	ComOwner = request.POST.get('ItemOwner')
    	ComOwnerFN = ""
    	ComOwnerState = "non-confirmed"

    else:
    	for account in request.user.socialaccount_set.all():
          ItemOwnerPrvdr = account.provider

          if ItemOwnerPrvdr == "facebook": 
		  ComOwner = account.extra_data['username']
		  ComOwnerFN = ""
		  ComOwnerState = "confirmed"
    	  elif ItemOwnerPrvdr == "twitter":
	    	  ComOwner = account.extra_data['screen_name']
	    	  ComOwnerFN = ""
	    	  ComOwnerState = "confirmed"
    	  elif ItemOwnerPrvdr == "google":
	    	  ComOwner = account.extra_data['name']
	    	  ComOwnerFN = account.extra_data['id']
	    	  ComOwnerState = "confirmed"
    	  elif ItemOwnerPrvdr == "persona":
	    	  ComOwner = account.user
	    	  ComOwnerFN = ""
	    	  ComOwnerState = "confirmed"
	  else:
	  	  pass

    ComContent = request.POST.get('comment')
    ComPubDate = timezone.now()
    
    list = get_object_or_404(List, slug=slug)
    p = Comment(
	NewComment = list, 
	ComContent = ComContent,
	ComOwnerState = ComOwnerState,
        ComOwner = ComOwner,
        ComPubDate = ComPubDate,
	)
    p.save()

    return HttpResponseRedirect(reverse('sopler:list', args=(list.slug,)))


#################################################
# Delete Comment
#################################################


def DeleteComment(request, slug):
    list = get_object_or_404(List, slug=slug)
    p = get_object_or_404(Comment, pk=int(request.POST['comment_pk']))
    p.delete()
    
    return HttpResponseRedirect(reverse('sopler:list', args=(list.slug,)))


#################################################
# Add New item to list
#################################################

def AddNewItem(request, slug):

    if request.user.is_anonymous():
    	ItemOwner = request.POST.get('ItemOwner')
        ItemOwnerState = "non-confirmed"
        ItemOwnerAvtr = ""
        ItemOwnerPrvdr = ""
        ItemOwnerFN = ""
        ItemOwnerLN = ""
        ItemOwnerLink = ""

    else:
    	for account in request.user.socialaccount_set.all():
          ItemOwnerPrvdr = account.provider

          if ItemOwnerPrvdr == "facebook": 
		  ItemOwner = account.extra_data['username']
                  ItemOwnerFN = account.extra_data['first_name']
                  ItemOwnerLN = account.extra_data['last_name']
                  ItemOwnerLink = account.extra_data['link']
		  ItemOwnerState = "confirmed"
		  ItemOwnerAvtr = account.get_avatar_url()

	  elif ItemOwnerPrvdr == "twitter":
	    	  ItemOwner = account.extra_data['screen_name']
                  ItemOwnerFN = account.extra_data['name']
                  ItemOwnerLN = ""
                  ItemOwnerLink = "https://twitter.com/" + account.extra_data['screen_name']
		  ItemOwnerState = "confirmed"
		  ItemOwnerAvtr = account.get_avatar_url()

	  elif ItemOwnerPrvdr == "google":
	    	  ItemOwner = account.extra_data['name']
                  ItemOwnerFN = account.extra_data['id']
                  ItemOwnerLN = ""
                  ItemOwnerLink = account.extra_data['link'] 
		  ItemOwnerState = "confirmed"
		  ItemOwnerAvtr = "https://plus.google.com/s2/photos/profile/" + account.extra_data['id'] + "?sz=100"
		  
	  elif ItemOwnerPrvdr == "persona":
	    	  ItemOwner = account.user
                  ItemOwnerFN = account.user
                  ItemOwnerLN = ""
                  ItemOwnerLink = "mailto:"+account.extra_data['email']
		  ItemOwnerState = "confirmed"
		  ItemOwnerAvtr = "/static/buttons/Persona.png"
	  else:
	  	  pass


    content = request.POST['content']
    ItemDone = False
    WhoDone = ""
    TimeDone = timezone.now()
    list = get_object_or_404(List, slug=slug)
    p = Item(
	list=list, 
	ItemOwner=ItemOwner,  
        ItemOwnerFN = ItemOwnerFN,
        ItemOwnerLN = ItemOwnerLN,
        ItemOwnerPrvdr = ItemOwnerPrvdr,
        ItemOwnerLink = ItemOwnerLink,
	content = content,
        ItemOwnerAvtr = ItemOwnerAvtr,
	ItemOwnerState = ItemOwnerState,
        TimeDone = TimeDone,
        WhoDone = WhoDone,
	ItemDone=ItemDone,
	)
    p.save()

    return HttpResponseRedirect(reverse('sopler:list', args=(list.slug,)))


#################################################
# Check item
#################################################
def CheckItem(request, slug):
    list = get_object_or_404(List, slug=slug)
    p = get_object_or_404(Item, pk=int(request.POST['item_pk']))
    p.ItemDone = True
    if p.ItemLocked == True :
      p.ItemDone = False
    else:
      if request.user.is_authenticated():
	
	for account in request.user.socialaccount_set.all():
          ItemOwnerPrvdr = account.provider

          if ItemOwnerPrvdr == "facebook": 
		  p.WhoDone = request.user.first_name + " " + request.user.last_name

	  elif ItemOwnerPrvdr == "twitter":
	    	  p.WhoDone = account.extra_data['screen_name']

	  elif ItemOwnerPrvdr == "google":
	    	  p.WhoDone = account.extra_data['name']
		  
	  elif ItemOwnerPrvdr == "persona":
	    	  p.WhoDone = account.user.username
	  else:
	  	  pass
          p.TimeDone = timezone.now()
          p.ItemMarked = False
      else:
          p.WhoDone = request.POST.get('ItemOwner')
          p.ItemMarked = False
    p.save()

    return HttpResponseRedirect(reverse('sopler:list', args=(list.slug,)))


#################################################
# Uncheck -already checked- item
#################################################
def UnCheckItem(request, slug):
    list = get_object_or_404(List, slug=slug)
    p = get_object_or_404(Item, pk=int(request.POST['item_pk']))
    if request.user.is_anonymous():
       if p.WhoDone == request.POST.get('ItemOwner'):
          p.ItemDone = False
          p.WhoDone = ""
       else :
          p.ItemDone = False

    else:

       if p.WhoDone == request.user.first_name + " " + request.user.last_name or p.ItemOwnerFN + " " + p.ItemOwnerLN == request.user.first_name + " " + request.user.last_name :
          p.ItemDone = False
          p.WhoDone = ""
       else :
          p.ItemDone = False
    p.save()

    return HttpResponseRedirect(reverse('sopler:list', args=(list.slug,)))

#################################################
# Delete Item From List
#################################################
def DeleteItem(request, slug):
    list = get_object_or_404(List, slug=slug)
    p = get_object_or_404(Item, pk=int(request.POST['item_pk']))
    if p.ItemLocked == True : 
       pass
    else:
       p.ItemDone = False
       p.delete()
    
    return HttpResponseRedirect(reverse('sopler:list', args=(list.slug,)))


#################################################
# Mark item, as important
#################################################
def MarkItem(request, slug):
    list = get_object_or_404(List, slug=slug)
    p = get_object_or_404(Item, pk=int(request.POST['item_pk']))
    if p.ItemLocked == False : 
       if p.ItemMarked == True : 
          p.ItemMarked = False 
       else:
          p.ItemMarked = True 
    else:
       if p.ItemMarked == True :
          pass
       else:
          pass
    p.save()

    return HttpResponseRedirect(reverse('sopler:list', args=(list.slug,)))

#################################################
# Lock an item, as important
#################################################
def LockItem(request, slug):
    list = get_object_or_404(List, slug=slug)
    p = get_object_or_404(Item, pk=int(request.POST['item_pk']))
    if p.ItemLocked == True :
       p.ItemLocked  = False
    else:
       p.ItemLocked  = True
    p.save()

    return HttpResponseRedirect(reverse('sopler:list', args=(list.slug,)))

