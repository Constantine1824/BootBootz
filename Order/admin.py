from django.contrib import admin
from .models import Order

list_display = ['tracking_id', 'status', 'created_at', 'updated_at']

admin.site.register(Order,list_display=list_display)

# Register your models here.
