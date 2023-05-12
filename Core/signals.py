from django.db.models.signals import post_save
from .models import Reviews
from django.dispatch import receiver

@receiver(post_save,sender=Reviews)
def rate(sender,instance,created, **kwargs):
    if created:
        product = instance.product
        reviews_obj = Reviews.objects.filter(product=product)
        stars = []
        for reviews in reviews_obj:
            stars.append(reviews.star)
        rating = 0
        number = 0
        #print(stars)
        for star in stars:
            number +=star
        rating = number / len(stars)
        product.rating = rating
        product.save()
            