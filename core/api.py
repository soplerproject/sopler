
from tastypie.resources import ModelResource
from core.models import List, Item
from tastypie import fields

      
class ItemResource(ModelResource):
    class Meta :
	list_allowed_methods = []
	detail_allowed_methods = ['get']
	include_resource_uri = False
	queryset = Item.objects.all()


class ListResource(ModelResource):
    item = fields.ToManyField('core.api.ItemResource','item_set', full=True)
    class Meta :
	include_resource_uri = False
	list_allowed_methods = []
	detail_allowed_methods = ['get']
	detail_uri_name = 'slug'
	excludes = ['id']
	queryset = List.objects.all()
	always_return_data = True
