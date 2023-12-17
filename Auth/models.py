from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import random

choices = (
    ('RESET','reset'),
    ('CONFIRM','Confirm')
)

class User(AbstractUser):
    is_verified = models.BooleanField(default=False)

    

class OneTimeToken(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    token = models.IntegerField(blank=False,null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10,choices=choices,default='CONFIRM')

    def is_valid(self):
        time_created = self.time_created.minute
        time_checked = datetime.datetime.now().minute
        duration = time_checked - time_created

        if duration <= 30:
            return True

    def generate_random_number(self):
        random_number = random.randrange(100_000,700_000)
        self.token = random_number


# Create your models here.
