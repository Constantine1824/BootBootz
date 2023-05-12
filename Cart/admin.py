from django.contrib import admin
from .models import Cart #CartItems

admin.site.register(Cart,list_display=['user'])
# admin.site.register(CartItems)
# Register your models here.
