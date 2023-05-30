"""BB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.documentation import SchemaGenerator

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="BootBootz",
        default_version='v1',
        description="API for BootBootz - an e-commerce website ",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ayomidet905@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('Core.urls'), name='core'),
    path('api/',include('Admin.urls'), name='admin'),
    path('api/auth/',include('Auth.urls')),
    #path('api/cart/',include('Cart.urls'), name='cart'),
    path('api/order/', include('Order.urls')),
    path('api/payments/',include('Payments.urls'),name='payments'),
    path('',schema_view.with_ui('swagger',cache_timeout=0))
    
]
