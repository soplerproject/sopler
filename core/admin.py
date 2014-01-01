# -*- coding: utf-8 -*-

from django.contrib import admin

from core.models import List, Item, Comment
from favit.models import Favorite

class TodoListAdmin(admin.ModelAdmin):
    list_display = ["ListName"]
    prepopulated_fields = {"slug": ("ListName",)}
    readonly_fields = ('id',)

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["user", "target_content_type", "target_object_id", "timestamp"]
    list_select_related = True
    search_fields = ("user__username", )
    raw_id_fields = ("user", )
    
admin.site.register(List, TodoListAdmin)
admin.site.register(Item)
admin.site.register(Comment)
admin.site.register(Favorite)
list_filter = ['ListPubDate']
