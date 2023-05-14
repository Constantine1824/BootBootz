from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError,ValidationError,AuthenticationFailed,NotAcceptable
from rest_framework.permissions import IsAuthenticated
from .serializers import UserCreationSerializer
from .models import User,OneTimeToken
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from django.core.signing import TimestampSigner,BadSignature
from datetime import timedelta


def get_signed_token(salt:str,value:str):
    signer = TimestampSigner(salt=salt)
    sign = signer.sign(value=value)
    return sign

def decode_signed_token(salt:str,value:str):
    signer = TimestampSigner(saalt=salt)
    try:
        sign = signer.unsign(value,max_age=timedelta(hours=1))
        return sign
    except BadSignature:
        raise AuthenticationFailed('Invalid token')


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
            # Block the user from accessing the account until the email is verified 
            user_obj.is_active = False
            user_obj.save()

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
                # Allow the user access to the account
                user = token.user
                user.is_active = True
                user.save()
                # Delete the token.... It has outlived its usefulness
                token.delete()
                signed_token = get_signed_token(salt='random',value=user.username)
                return Response({
                    'detail' : "Verified!",
                    'auth_token' : signed_token
                })
            raise ParseError("Invalid Token")
        except OneTimeToken.DoesNotExist:
            raise ParseError('Token does not exist')
        

class PasswordChangeApiView(APIView):
    """This view should handle requests to change the password for the given user
    It should be protected to prevent direct access to it without passing the earlier views
    But for now it will just change the password without any confirmation if the email has been confirmed
    """
    def post(self,request):
        try:
            password = request.data['password']
            if request.user.is_authenticated:
            # For authenticated users requesting a password change
                user = request.user
                user.password = password
                user.save()
                return Response({
                    'detail' : 'Password changed'
                }, status=status.HTTP_200_OK)
            try:
                username = request.data['username']
                try:
                    signed_token = request.META.get('Signed_token')
                    decoded_username = decode_signed_token(salt='random',value=signed_token)
                    user = User.objects.get(username=username)
                    if user.username != decoded_username:
                        raise ParseError('')
                    user.password = password
                    user.save()
                    return Response({
                    'detail' : 'Password changed'
                     }, status=status.HTTP_200_OK)
                except KeyError:
                    raise NotAcceptable('Signature header must be set')
                except User.DoesNotExist:
                    raise ValidationError('Username is not valid')
            except KeyError:
                raise ParseError('Username is required')
        except KeyError:
            raise ValidationError("Password must be provided")
        

# Create your views here.
