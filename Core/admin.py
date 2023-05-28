from django.contrib import admin
from .models import Address,Boots,Reviews,Variants

products_list = ['name','manufacturer','category','price','date_added']

address_list = ['user','city','state']

admin.site.register(Boots,list_display=products_list)
admin.site.register(Address,list_display=address_list)
admin.site.register(Reviews,list_display=['user','star'])
admin.site.register(Variants,list_display=['quantity_available','color'])
# Register your models here.
