from django.db import models
from Core.models import Address, Variants
from Auth.models import User
from django.utils.timezone import now
import random
import string

class Order(models.Model):
    Pending = 'PEN'
    Approved = 'APR'
    Delivered = 'DEL'
    status_codes = (
        (Pending,'Pending'),
        (Approved,'Approved'),
        (Delivered,'Delivered')
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    tracking_id = models.CharField(max_length=18,blank=True)
    status = models.CharField(max_length=15, choices=status_codes)
    delivery_fee = models.DecimalField(default=210.00,decimal_places=2,max_digits=7)
    created_at = models.DateTimeField(default=now())
    updated_at = models.DateTimeField(auto_now=True)
    delivery_address = models.ForeignKey(Address,null=True, on_delete=models.SET_NULL)
    total_price = models.DecimalField(decimal_places=2)

    def save(self,*args, **kwargs):
        tracking_id = ''.join(random.choices(string.ascii_uppercase + string.digits,k=15))
        while Order.objects.filter(tracking_id=tracking_id).exists():
            tracking_id = ''.join(random.choices(string.ascii_uppercase + string.digits +string.ascii_lowercase,k=15))
        self.tracking_id = tracking_id
        super(Order,self).save(*args, **kwargs)


    def __str__(self):
        return self.tracking_id

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderItems')
    product = models.OneToOneField(Variants, on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    discount = models.IntegerField(default=0)

    def __str__(self):
        return self.order
# Create your models here.
