from django.urls import path
from .views import (SignupApiView,EmailSendApiView,EmailVerifyApiView,
                    PasswordResetEmailAPIView,PasswordResetConfirmAPIview,
                    PasswordChangeApiView
                    )
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('signup',SignupApiView.as_view(), name='signup'),
    path('token', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh',TokenRefreshView.as_view(), name='refresh'),
    path('verify-email', EmailSendApiView.as_view(), name='send mail'),
    path('verify-email/verify',EmailVerifyApiView.as_view(), name='verify mail'),
    path('reset-passsword/initialize',PasswordResetEmailAPIView.as_view(),name='reset password'),# Initialize password reset
    path('reset-password/confirm',PasswordResetConfirmAPIview.as_view(), name='confirm reset'),
    path('reset-password',PasswordChangeApiView.as_view(),name='change password')
]
