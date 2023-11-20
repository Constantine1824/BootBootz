from django.urls import path
from .views import DeleteFromCartAPIView, CartApiView

urlpatterns = [
    path('', CartApiView.as_view(), name='cart_opts'),
    path('remove',DeleteFromCartAPIView.as_view(), name='remove from cart')
]
