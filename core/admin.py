# -*- coding: utf-8 -*-

from django.contrib import admin
from core.models import List, Item, Comment

class TodoListAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("ListName",)}
    readonly_fields = ('id',)

admin.site.register(List, TodoListAdmin)
admin.site.register(Item)
admin.site.register(Comment)
list_filter = ['ListPubDate']
