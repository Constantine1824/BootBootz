from django.urls import path
from .views import (NewArrivalsApiView,AllProductsApiView,SearchApiView,CreateAddressApiView,
                    ProductsRetrieveApiView,CategoryAPIView,MakerAPIView,ReviewsAPIView)

urlpatterns = [
    path('all',AllProductsApiView.as_view(), name='all'),
    path("newArrivals",NewArrivalsApiView.as_view(),name='latest'),
    path('search',SearchApiView.as_view(),name='search'),
    path('address/create',CreateAddressApiView.as_view(), name='create address'),
    path('view/<slug:slug>',ProductsRetrieveApiView.as_view(), name='view'),
    path('categories/<str:pk>',CategoryAPIView.as_view(),name='catgories'),
    path('manufacturer/<str:pk>',MakerAPIView.as_view(), name='manufacturer'),
    path('reviews',ReviewsAPIView.as_view(),name='reviews')
]

