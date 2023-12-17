from threading import Thread
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import OneTimeToken

class EmailThread(Thread):
    def __init__(self, email):
        self.email = email
        super().__init__()

    def run(self):
        self.email.send()

async def send_verification_mail(user, token):
    context= {'user': user.first_name, 'token': token}
    message = render_to_string('email/verify.html', context=context)
    email = EmailMessage(
        'Verify your account for BreeZe',
        message,
        to = [user.email]
    )
    email.content_subtype = 'html'
    await EmailThread(email).start()

async def send_password_reset_mail(user, token):
    context = {
        'user' : user.first_name,
        'token' : token
    }
    message = render_to_string('email/reset_password.html', context=context)
    email = EmailMessage(
        'Request for a password change',
        message,
        to=[user.email]
    )
    email.content_subtype = 'html'
    await EmailThread(email).start()
    