# -*- coding: utf-8 -*-

from django.contrib import admin

from core.models import List, Item, Comment
from favit.models import Favorite


class ListAdmin(admin.ModelAdmin):
    list_display = ["ListName","slug","ListOwner","ListOwnerState", "ListPubDate"]
    search_fields = ("ListName","slug","ListOwner")


class ItemAdmin(admin.ModelAdmin):
    list_display = ["list_ListName","list_slug","ItemOwner"]
    search_fields = ("ItemOwner","list__ListName","list_slug",)
    
    def list_ListName(self, instance):
        return instance.list.ListName
        
    def list_slug(self, instance):
        return instance.list.slug  

        
class CommentAdmin(admin.ModelAdmin):
    list_display = ["NewComment_ListName","NewComment_slug","ComOwner","ComContent"]
    search_fields = ("ComOwner","NewComment__ListName","NewComment__slug",)
    
    def NewComment_ListName(self, instance):
        return instance.NewComment.ListName
        
    def NewComment_slug(self, instance):
        return instance.NewComment.slug

        
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["user", "target_content_type", "target_object_id", "timestamp"]
    list_select_related = True
    search_fields = ("user__username", )
    raw_id_fields = ("user", )

    
admin.site.register(List, ListAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Favorite, FavoriteAdmin)
