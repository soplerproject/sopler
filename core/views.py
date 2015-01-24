# -*- coding: utf-8 -*-

import hashlib
import time
import random
import re

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import DetailView, TemplateView, ListView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Sopler Models
from core.models import List, Item, Comment

# Social Friends Finder (Models, Utils)
from social_friends_finder.models import SocialFriendList
from social_friends_finder.utils import setting

# Allauth Models
import allauth.socialaccount.models

# Favit Models
from favit.models import Favorite

#################################################
# Config
#################################################

pages_dir = "pages/"

if setting("SOCIAL_FRIENDS_USING_ALLAUTH", False):
    USING_ALLAUTH = True
else:
    USING_ALLAUTH = False
    
REDIRECT_IF_NO_ACCOUNT = setting('SF_REDIRECT_IF_NO_SOCIAL_ACCOUNT_FOUND', False)
REDIRECT_URL = setting('SF_REDIRECT_URL', "/")

#################################################

class FriendListView(ListView):
  
    model = List
    template_name = pages_dir + "index.html"
    
    def get(self, request, provider=None):

        if request.user.is_anonymous() :
	  self.social_auths = ""
	  self.social_friend_lists = []
	  self.social_user_lists = []
	  self.social_friend_lists = SocialFriendList.objects.get_or_create_with_social_auths(self.social_auths)
	  return super(FriendListView, self).get(request)
	
	else:
	  if USING_ALLAUTH:
	      self.social_auths = request.user.socialaccount_set.all()
	  else:
	      self.social_auths = request.user.social_auth.all() 
	  self.social_friend_lists = []
	  self.social_user_lists = []
	  # for each social network, get or create social_friend_list
	  self.social_friend_lists = SocialFriendList.objects.get_or_create_with_social_auths(self.social_auths)
	  return super(FriendListView, self).get(request)
      
    def get_context_data(self, **kwargs):
        context = super(FriendListView, self).get_context_data(**kwargs)

        friends = []
        for friend_list in self.social_friend_lists:
            fs = friend_list.existing_social_friends()
            for f in fs:
                friends.append(f)

        # Print Friends
        context['friends'] = friends
        
        # Print All users
	context['users'] = User.objects.all()
	
	# Print All lists
	model = List
	context['lists'] = List.objects.all()

        connected_providers = []
        for sa in self.social_auths:
            connected_providers.append(sa.provider)
        context['connected_providers'] = connected_providers

        return context
      
      
class ViewProfilePage(TemplateView):
    template_name = pages_dir + "dosignin.html"
    
    
class ViewList(DetailView):
    model = List
    template_name = pages_dir + "sidepanel.html"
    
    def get_context_data(self, **kwargs):
      context = super(ViewList, self).get_context_data(**kwargs)
      context['lists'] = List.objects.all()
      context['users'] = User.objects.all()
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
		  ListOwnerLink = "https://plus.google.com/" + account.extra_data['id']
		  
	  elif ListOwnerPrvdr == "persona":
	    	  ListOwner   = account.user
                  ListOwnerFN = ""
                  ListOwnerLN = ""
		  ListOwnerState = "confirmed"
		  ListOwnerLink = "" 
	  else:
	  	  pass

    req = request.POST['ListName'].encode('utf-8')
    
    # Allow authenticated users only
    ListAuthOnly = request.POST.get('ListAuthOnly')
    if ListAuthOnly: 
        ListAuthOnly = True
        ListIsPrivate = False
        ListIsHidden = False
    else:
        ListAuthOnly = False
        
    #Set this list as private
    ListIsPrivate = request.POST.get('ListIsPrivate') 
    if ListIsPrivate: 
        ListIsPrivate = True
        ListAuthOnly = False
        ListIsHidden = False
    else:
        ListIsPrivate = False
        
    # Set this list as hidden
    ListIsHidden = request.POST.get('ListIsHidden') 
    if ListIsHidden: 
        ListIsHidden = True
        ListAuthOnly = False
        ListIsPrivate = False
    else:
        ListIsHidden = False
        
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
	ListIsPrivate = ListIsPrivate,
	ListIsHidden = ListIsHidden,
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
# Set List as Private.
#################################################

def SetItPrivate(request, slug):
    p = get_object_or_404(List, slug=slug)
    if p.ListIsPrivate: 
      p.ListIsPrivate = False
    else:
      p.ListIsPrivate = True
      p.ListAuthOnly = False
      p.ListIsHidden = False
    p.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
  
#################################################
# Set List as Hidden.
#################################################

def SetItHidden(request, slug):
    p = get_object_or_404(List, slug=slug)
    if p.ListIsHidden: 
      p.ListIsHidden = False
    else:
      p.ListIsHidden = True
      p.ListAuthOnly = False
      p.ListIsPrivate = False
    p.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

#################################################
# Allow authenticated users only. 
#################################################

def SetAuthOnly(request, slug):
    p = get_object_or_404(List, slug=slug)
    if p.ListAuthOnly: 
      p.ListAuthOnly = False
    else:
      p.ListAuthOnly = True
      p.ListIsHidden = False
      p.ListIsPrivate = False
    p.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

#################################################
# Delete List
#################################################

def DeleteList(request, slug):
    p = get_object_or_404(List, slug=slug)
    p.delete()
    
    return HttpResponseRedirect('/lists/')


#################################################
# Delete Previous Lists
#################################################

def DeletePreviousList(request, slug):
    p = get_object_or_404(List, slug=slug)
    p.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


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
		  ItemOwnerAvtr = "https://graph.facebook.com/" + account.extra_data['id'] + "/picture?type=large"

	  elif ItemOwnerPrvdr == "twitter":
	    	  ItemOwner = account.extra_data['screen_name']
                  ItemOwnerFN = account.extra_data['name']
                  ItemOwnerLN = ""
                  ItemOwnerLink = "https://twitter.com/" + account.extra_data['screen_name']
		  ItemOwnerState = "confirmed"
		  ItemOwnerAvtr = account.extra_data['profile_image_url_https']

	  elif ItemOwnerPrvdr == "google":
	    	  ItemOwner = account.extra_data['name']
                  ItemOwnerFN = account.extra_data['id']
                  ItemOwnerLN = ""
                  ItemOwnerLink = "https://plus.google.com/" + account.extra_data['id'] 
		  ItemOwnerState = "confirmed"
		  ItemOwnerAvtr = account.extra_data['picture']
		  
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
    
    p.ItemDone = False
    p.WhoDone = ""
    p.ItemDueDate = None
    p.save()
    
    return HttpResponseRedirect(reverse('sopler:list', args=(list.slug,)))

#################################################
# Edit an item
#################################################

def EditItem(request, slug):
    list = get_object_or_404(List, slug=slug)
    p = get_object_or_404(Item, pk=int(request.POST['item_pk']))
    
    p.content = request.POST['EditContents']
    p.save()
    
    return HttpResponseRedirect(reverse('sopler:list', args=(list.slug,)))

#################################################
# Set Due Date to item
#################################################

def SetItemDueDate(request, slug):
    list = get_object_or_404(List, slug=slug)
    p = get_object_or_404(Item, pk=int(request.POST['item_pk']))
    
    p.ItemDueDate = request.POST['SetDueDate']
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
     
    elif p.ItemOwnerState == "non-confirmed":
	p.ItemDone = False
	p.delete()
	
    else:
       if request.user.is_authenticated():
	for account in request.user.socialaccount_set.all():
          ItemOwnerPrvdr = account.provider
          
          if ItemOwnerPrvdr == "facebook": 
	    if p.ItemOwner == account.extra_data['username'] or list.ListOwner == account.extra_data['username']:
	      p.ItemDone = False
	      p.delete()
	      
	  elif ItemOwnerPrvdr == "twitter":
	    if p.ItemOwner == account.extra_data['screen_name'] or list.ListOwner == account.extra_data['screen_name']:
	      p.ItemDone = False
	      p.delete()
	      
	  elif ItemOwnerPrvdr == "google":
	    if p.ItemOwner == account.extra_data['name'] or list.ListOwner == account.extra_data['name']:
	      p.ItemDone = False
	      p.delete()
	      
	  elif ItemOwnerPrvdr == "persona":
	    if p.ItemOwner == account.user.username or list.ListOwner == account.user.username:
	      p.ItemDone = False
	      p.delete()
	  else:
	    pass
	else:
	  pass
      
    return HttpResponseRedirect(reverse('sopler:list', args=(list.slug,)))
  
#################################################
# Mark item, as important
#################################################

def MarkItem(request, slug):
    list = get_object_or_404(List, slug=slug)
    p = get_object_or_404(Item, pk=int(request.POST['item_pk']))
    list = get_object_or_404(List, slug=slug)
			  
    if request.user.is_authenticated():
      
      if p.ItemOwnerState == "non-confirmed":
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

      else:
	for account in request.user.socialaccount_set.all():
	  ItemOwnerPrvdr = account.provider
	  
	  if ItemOwnerPrvdr == "facebook": 
	    if p.ItemOwner == account.extra_data['username'] or list.ListOwner == account.extra_data['username'] :
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
	      
	  elif ItemOwnerPrvdr == "twitter":
	    if p.ItemOwner == account.extra_data['screen_name'] or list.ListOwner == account.extra_data['screen_name']:
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
	      
	  elif ItemOwnerPrvdr == "google":
	    if p.ItemOwner == account.extra_data['name'] or list.ListOwner == account.extra_data['name']:
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
	      
	  elif ItemOwnerPrvdr == "persona":
	    if p.ItemOwner == account.user.username or list.ListOwner == account.user.username:
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
	  else:
	    pass
    else:
      if p.ItemOwnerState == "non-confirmed":
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
      else:
	pass

    return HttpResponseRedirect(reverse('sopler:list', args=(list.slug,)))

#################################################
# Lock an item, as important
#################################################

def LockItem(request, slug):
    list = get_object_or_404(List, slug=slug)
    p = get_object_or_404(Item, pk=int(request.POST['item_pk']))
    
    if request.user.is_authenticated():
      if p.ItemOwnerState == "non-confirmed":
	if p.ItemLocked == True :
	  p.ItemLocked  = False
	else:
	  p.ItemLocked  = True
	p.save()
      else:
	for account in request.user.socialaccount_set.all():
	  ItemOwnerPrvdr = account.provider
	  
	  if ItemOwnerPrvdr == "facebook":
	    if p.ItemOwner == account.extra_data['username'] or list.ListOwner == account.extra_data['username'] :
	      if p.ItemLocked == True :
		p.ItemLocked  = False
	      else:
		p.ItemLocked  = True
	      p.save()
	      
	  elif ItemOwnerPrvdr == "twitter":
	    if p.ItemOwner == account.extra_data['screen_name'] or list.ListOwner == account.extra_data['screen_name']:
	      if p.ItemLocked == True :
		p.ItemLocked  = False
	      else:
		p.ItemLocked  = True
	      p.save()
	      
	  elif ItemOwnerPrvdr == "google":
	    if p.ItemOwner == account.extra_data['name'] or list.ListOwner == account.extra_data['name']:
	      if p.ItemLocked == True :
		p.ItemLocked  = False
	      else:
		p.ItemLocked  = True
	      p.save()
	      
	  elif ItemOwnerPrvdr == "persona":
	    if p.ItemOwner == account.user.username or list.ListOwner == account.user.username:
	      if p.ItemLocked == True :
		p.ItemLocked  = False
	      else:
		p.ItemLocked  = True
	      p.save()
	  else:
	    pass
    else:
      if p.ItemOwnerState == "non-confirmed":
	if p.ItemLocked == True :
	  p.ItemLocked  = False
	else:
	  p.ItemLocked  = True
	p.save()
      else:
	pass

    return HttpResponseRedirect(reverse('sopler:list', args=(list.slug,)))
    

#################################################
# Favorite a list 
#################################################  

@login_required
def favit(request,slug):
        
    list = get_object_or_404(List, slug=slug)
    user = request.user

    slug = List.objects.get(slug=request.POST["slug"])
    fav = Favorite.objects.get_favorite(user, slug) 
      
    if fav is None:
	fav = Favorite.objects.create(user, slug)
	
    else:
	fav.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    