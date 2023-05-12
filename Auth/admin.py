from django.contrib import admin
from .models import User,OneTimeToken

admin.site.register(User)
admin.site.register(OneTimeToken)

# Register your models here.
