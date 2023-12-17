from django.db.models.signals import post_save
from .models import User, OneTimeToken
from django.dispatch import receiver
from .email import send_verification_mail

@receiver(post_save, sender=User)
async def verification_mail(sender, instance, created, **kwargs):
    if created:
        token_obj = OneTimeToken(user=instance, type='CONFIRM')
        token_obj.generate_random_number()
        token_obj.save()
        await send_verification_mail(instance, token_obj.token)