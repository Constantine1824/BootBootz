from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import OrderViewSets,ProductViewSets

router = DefaultRouter()

router.register('products',ProductViewSets,'products')
router.register('order',OrderViewSets,'order')

urlpatterns = [
    path('admin/',include(router.urls),name='admin api')
]

