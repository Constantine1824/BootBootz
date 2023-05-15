from django.urls import path
from .views import (NewArrivalsApiView,AllProductsApiView,SearchApiView,CreateAddressApiView,
                    ProductsRetrieveApiView,CategoryAPIView,MakerAPIView,ReviewsAPIView,VariantsListApiView)

urlpatterns = [
    path('all',AllProductsApiView.as_view(), name='all'),
    path("newArrivals",NewArrivalsApiView.as_view(),name='latest'),
    path('search',SearchApiView.as_view(),name='search'),
    path('address/create',CreateAddressApiView.as_view(), name='create address'),
    path('view/<slug:slug>',ProductsRetrieveApiView.as_view(), name='view'),
    path('view/variants/<str:pk>',VariantsListApiView.as_view(),name='variants list'),
    path('categories/<str:pk>',CategoryAPIView.as_view(),name='categories'),
    path('manufacturer/<str:pk>',MakerAPIView.as_view(), name='manufacturer'),
    path('reviews',ReviewsAPIView.as_view(),name='reviews')
]

