from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from .serializers import UserCreationSerializer
from .models import User,OneTimeToken
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status


class SignupApiView(APIView):
    def post(self,request):
        data = request.data
        if data['password'] != data['password2']:
            raise ParseError('Passwords do not match')
        serializer = UserCreationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        
class EmailSendApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        email = request.user.email
        username = request.user.username
        user = User.objects.get(username=username)
        token = OneTimeToken.objects.create(user=user)
        token.generate_random_number()
        token.save()
        subject = f"Verify email Address for " + email
        message = "Your verification code is " + f"{token.token}" + "Please Note that this is only valid for 30minutes\
                    Thank you! from the Bootz Team"
        html_message = f"<p>Your Verification code is {token.token}</p>\
                <p>Please note that this will expire in <em>30minutes</em><p/>"
        to = [email]
        from_email = settings.EMAIL_HOST_USER
        try:
            send_mail(subject,
                      message,
                      from_email=from_email,
                      recipient_list = to,
                      html_message=html_message,
                      fail_silently=False)
            return Response({
            'token' : token.token,
            "detail" : 'email sent'
        },status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response(
                {'detail':'Failed',
                 },status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
          
class EmailVerifyApiView(APIView):
    def post(self,request):
        token = request.data['token']
        try:
            token_obj = OneTimeToken.objects.get(token=token,type='CONFIRM')
            if token_obj.is_valid(30):
                user = token_obj.user
                user.is_verified = True
                user.save()
                token_obj.delete()
                return Response({
                        'status' : "Token verified",
                        'user' : user.username
                    })
            else:
                token_obj.delete()
                return Response({
                        'status' : "Token has expired!"
                    })
        except OneTimeToken.DoesNotExist:
            raise ParseError('Invalid Token')

class PasswordResetEmailAPIView(APIView):
    def post(self,request):
        email = request.POST['email']
        try:
            user_obj = User.objects.get(email=email)
            
            token = OneTimeToken(user=user_obj,type='RESET')
            token.generate_random_number()
            token.save()
            subject = f"""
                    Reset password for {user_obj.username}
            """
            message = f"""
                Your password reset code is {token.token}
                please note that this token will expire in 30 minutes
            """
            to = [email]
            try:
                send_mail(
                    subject,
                    message,
                    to=to,
                    fail_silently=False
                )
            except Exception as e:
                return Response(
                    {"detail": "Failed to send mail",
                    "reason" : e
                    },
                )
            return Response({
                'token' : token,
                'detail' : 'email sent!'
            })
        except User.DoesNotExist:
            raise ParseError('User with the given email does not exist!')
     
class PasswordResetConfirmAPIview(APIView):
    def post(self,request):
        token_ = request.data['token']
        try:
            token = OneTimeToken.objects.get(token=token_,type='RESET')
            if token.is_valid():
                return Response({
                    'detail' : "Verified!"
                })
            raise ParseError("Invalid Token")
        except OneTimeToken.DoesNotExist:
            raise ParseError('Token does not exist')
# Create your views here.
