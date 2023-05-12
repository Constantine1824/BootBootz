from django.db import models
from Core.models import Address
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
    order_summary = models.JSONField(null=True)
    status = models.CharField(max_length=15, choices=status_codes)
    delivery_fee = models.DecimalField(default=210.00,decimal_places=2,max_digits=7)
    created_at = models.DateTimeField(default=now())
    updated_at = models.DateTimeField(auto_now=True)
    delivery_address = models.ForeignKey(Address,null=True, on_delete=models.SET_NULL)

    def save(self,*args, **kwargs):
        tracking_id = ''.join(random.choices(string.ascii_uppercase + string.digits,k=15))
        while Order.objects.filter(tracking_id=tracking_id).exists():
            tracking_id = ''.join(random.choices(string.ascii_uppercase + string.digits +string.ascii_lowercase,k=15))
        self.tracking_id = tracking_id
        super(Order,self).save(*args, **kwargs)


    def __str__(self):
        return self.tracking_id
# Create your models here.
