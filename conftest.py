import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def products_obj():
    from Core.models import Products
    return Products.objects.all()

@pytest.fixture
def create_user(django_user_model,db):
    def create(**kwargs):
        return django_user_model.objects.create_user(**kwargs)
    return create

@pytest.fixture
def get_token(django_user_model,db):
    data = {
        'username' : 'aetaiwo',
        'password' : 'Constant'
    }
    client = APIClient()
    user = django_user_model.objects.create_user(username='aetaiwo',password='Constant')
    url = reverse('login')
    response = client.post(url,data=data)
    access_token = response.json()['access']
    return access_token
