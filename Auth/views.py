from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from .serializers import UserCreationSerializer
from .models import User,OneTimeToken
from .signals import verification_mail
from .email import send_verification_mail, send_password_reset_mail

class SignupApiView(APIView):
    def post(self,request):
        data = request.data
        if data['password'] != data['password2']:
           return Response(
               {
                   'status' : 'error',
                   'detail' : "Passwords don't match"
               },
               status = status.HTTP_400_BAD_REQUEST
           )
        serializer = UserCreationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(
            {
                'status' : 'success',
                'detail' : 'User created',
                'data' : serializer.data
            }
            ,status=status.HTTP_201_CREATED)
        

class EmailSendApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        token_obj = OneTimeToken.objects.get(user=request.user, type='CONFIRM')
        if not token_obj.is_valid():
            token_obj = OneTimeToken.objects.create(user=request.user, type='CONFIRM')
        token_obj.generate_random_number()
        token = token_obj.token
        send_verification_mail(request.user, token=token)
        return Response(
            {
                'status' : 'success',
                'detail' : 'New email confirm token sent'
            },
            status = status.HTTP_200_OK
        )
          

class EmailVerifyApiView(APIView):
    def post(self,request):
        token = request.data['token']
        try:
            token_obj = OneTimeToken.objects.get(token=token,type='CONFIRM')
            if token_obj.is_valid():
                user = token_obj.user
                user.is_verified = True
                user.save()
                token_obj.delete()
                return Response({
                        'status' : "Success",
                        'detail' : 'Account verification successful',
                        'user' : user.username
                    },
                    status=status.HTTP_200_OK
                    )
            else:
                token_obj.delete()
                return Response({
                        'status' : "fail",
                        'detail' : 'Token has expired'
                    })
        except OneTimeToken.DoesNotExist:
           return Response({
               'status' : 'error',
               'detail' : 'Token does not exist'
           },
           status = status.HTTP_400_BAD_REQUEST
           )


class PasswordResetEmailAPIView(APIView):
    async def post(self,request):
        email = request.POST['email']
        try:
            user_obj = User.objects.get(email=email)
            token = OneTimeToken(user=user_obj,type='RESET')
            token.generate_random_number()
            token.save()
            await send_password_reset_mail(user_obj, token.token)
            return Response(
                {
                    'status' : 'success',
                    'detail' : 'Reset email sent'
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({
                'status' : 'error',
                'detail' : str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
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
                return Response({
                    'status' : 'success',
                    'detail' : "Account Verified",
                })
        except OneTimeToken.DoesNotExist:
            return Response(
                {
                    'status' : 'fail',
                    'detail' : "User doesn't exist"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        

class PasswordChangeApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            if not request.user.is_active():
                return Response({
                    'status' : 'fail',
                    'detail' : 'Email has not been verified for this change'
                })
            password = request.data['password']
            user = request.user
            user.password = password
            user.save()
            return Response({
                'detail' : 'Password changed'
            }, status=status.HTTP_200_OK)

        except KeyError:
            raise ValidationError("Password must be provided")
        

# Create your views here.
