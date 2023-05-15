from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.conf import settings
import random
import string, datetime

User = settings.AUTH_USER_MODEL

class Address(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=355)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username + " " + self.city


class Boots(models.Model):
    category_choices = (
        ('K','Kids'),
        ('M', 'Men'),
        ('W', 'Women')
    )
    status = (
        ('A',_('Available')),
        ('U',_('Unavailable')),
        ('R',_('Restocked'))
    )
    name = models.CharField(max_length=255)
    size = models.ManyToManyField('Size')
    price = models.DecimalField(max_digits=9,decimal_places=2)
    manufacturer = models.CharField(max_length=100)
    default_img = models.FileField(upload_to='media/default')
    category = models.CharField(max_length=255, choices=category_choices)
    slug = models.SlugField(blank=True)
    availability_status = models.CharField(max_length=24,choices=status)
    date_added = models.DateTimeField(default=datetime.datetime.now())
    newly_added = models.BooleanField(default=True)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Boots'

    def save(self, *args, **kwargs):
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        slug = slugify(self.name + '+' + self.category + "" + random_str)
        while Boots.objects.filter(slug=slug).exists():
            random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
            slug = slugify(slug + '' + random_str) 
        self.slug = slug
        super(Boots, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + " " + self.manufacturer

class BootsVariants(models.Model):
    boot = models.ForeignKey(Boots,on_delete=models.CASCADE)
    quantity_available = models.IntegerField()
    color = models.CharField(max_length=23,blank=False)
    image_1 = models.FileField(upload_to='media')
    image_2 = models.FileField(upload_to='media',blank=True)
    image_3 = models.FileField(upload_to='media',blank=True)

    def __str__(self):
        return self.color + ' | ' + self.boot.name

    class Meta:
        verbose_name_plural = 'Boots Variants'

class Reviews(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Boots,on_delete =models.CASCADE)
    star = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return f'{self.star}'
    
    class Meta:
        verbose_name_plural = 'Reviews'

class Size(models.Model):
    size = models.IntegerField()

    def __str__(self):
        return f'{self.size}'

# Create your models here.