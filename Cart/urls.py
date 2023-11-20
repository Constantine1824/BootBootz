from django.urls import path
from .views import DeleteFromCartAPIView, CartApiView, ClearCartAPIView

urlpatterns = [
    path('', CartApiView.as_view(), name='cart_opts'),
    path('remove/<int:pk>',DeleteFromCartAPIView.as_view(), name='remove from cart'),
    path('clear', ClearCartAPIView.as_view(), name='clear cart')
]
