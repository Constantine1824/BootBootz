from django.db import models
from Core.models import Products
from Auth.models import User

class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    products = models.ManyToManyField(Products,related_name='cart')

    def __str__(self):
        return self.user.username


# class CartItems(models.Model):
#     cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
#     products = models.ForeignKey(Products,on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     date_added = models.DateTimeField(auto_now_add=True)
# Create your models here.
