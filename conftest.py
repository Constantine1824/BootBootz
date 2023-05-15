import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def products_obj():
    from Core.models import Boots
    Boots.objects.create(name='Nike XZ2',price=142.24,manufacturer='Nike',category='M',)
    Boots.objects.create(name='BLW',price=162.27,manufacturer='Adidas',category='F',)
    Boots.objects.create(name='Nike Air Max',price=149.28,manufacturer='Nike',category='M',)
    Boots.objects.create(name='Tross',price=104.29,manufacturer='New Balance',category='K',)
    return Boots

@pytest.fixture
def create_user(django_user_model,db):
    def create(**kwargs):
        return django_user_model.objects.create_user(**kwargs)
    return create

@pytest.fixture
def get_token(django_user_model,db):
    data = {
        'username' : 'aetaiwo',
        'password' : 'Constant',
    }
    client = APIClient()
    user = django_user_model.objects.create_user(username='aetaiwo',password='Constant',is_verified=True)
    url = reverse('login')
    response = client.post(url,data=data)
    access_token = response.json()['access']
    return access_token
