from django.db import models
from Core.models import Boots, TimeStampedField, Variants
from Auth.models import User

class Cart(TimeStampedField):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    


class CartItems(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='cartItems')
    boot = models.OneToOneField(Variants,on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.cart
    
    class Meta:
        verbose_name_plural = 'CartItems'
# Create your models here.
