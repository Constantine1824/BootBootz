from django.test import TestCase
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .serializers import BootsSerializer,BootsVariantsSerializer
import Core.signals
from Auth.models import AbstractUser,User
from urllib.parse import urlencode
from django.db.models import Q
import pytest


class TestProductsView:
    @pytest.mark.django_db
    def test_all_products(self,products_obj,api_client):
        client = api_client
        products = products_obj.objects.all()
        serializer = BootsSerializer(products,many=True)
        url = reverse('all')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # assert response.data == serializer.data # Not working with pagination.....
        assert len(serializer.data) == 4

    @pytest.mark.django_db
    def test_products_retrieval(self,products_obj,api_client):
        # Get first products
        boots_obj = products_obj.objects.get(id=1)
        slug = boots_obj.slug 
        url = reverse(f'view', kwargs={
            'slug' : slug
        })
        serializer = BootsSerializer(boots_obj)
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.json() == serializer.data

    @pytest.mark.django_db
    def test_variants_retrieval(self,products_obj,api_client):
        boots_obj = products_obj.objects.get(id=1)
        name = boots_obj.name
        variants = boots_obj.bootsvariants_set.all()
        serializer = BootsVariantsSerializer(variants,many=True)
        url = reverse('variants list', kwargs={
            'pk' : name
        })
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.json() == serializer.data
        assert len(serializer.data) == 0

    @pytest.mark.django_db
    def test_new_arrival(self,products_obj,api_client):
        products = products_obj.objects.filter(newly_added=True)
        serializer = BootsSerializer(products,many=True)
        url = reverse('latest')
        response = api_client.get(url)
        assert response.json() == serializer.data
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_search(self,api_client,products_obj):
        query = 'Nike'
        products_query = products_obj.objects.filter(
                Q(name__icontains=query)|
                Q(category__icontains=query)|
                Q(manufacturer__icontains=query)
            )
        serializer = BootsSerializer(products_query,many=True)
        q = {
            'q' : query
        }
        urlized_q = urlencode(q)
        print(urlized_q)
        url = reverse('search') #f'api/search{urlized_q}'
        response = api_client.get(f'{url}?{urlized_q}')
        assert response.status_code == 200
        assert response.json() == serializer.data
    
    @pytest.mark.django_db
    def test_categories(self,api_client,products_obj):
        products = products_obj.objects.filter(category='M')
        serializer = BootsSerializer(products,many=True)
        url = reverse('categories',kwargs={
            'pk' : 'M'
        })
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.json() == serializer.data

    @pytest.mark.django_db
    def test_maker(self,api_client,products_obj):
        product = products_obj.objects.filter(manufacturer='Nike')
        serializer = BootsSerializer(product,many=True)
        url = reverse('manufacturer',kwargs={
            'pk' : 'Nike'
        })
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.json() == serializer.data

    @pytest.mark.django_db
    def test_address(self,api_client,get_token):
        access_token = get_token
        url = reverse('create address')
        client = api_client
        client._credentials = {
                'HTTP_AUTHORIZATION' : f'Bearer {access_token}'
            }
        data = {
            'user' : 'aetaiwo',
            'address' : 'No 1, Ohimege Road, Ilorin',
            'city' : 'Ilorin',
            'state' : 'Kwara'
        }
        response = client.post(url,data=data)
        assert response.status_code == 201
        assert response.json()['city'] == 'Ilorin'

    @pytest.mark.django_db
    def test_review_creation(self,get_token,products_obj,api_client):
        access_token = get_token
        product = products_obj.objects.get(id=2)
        product_name = product.name
        data = {
            'product' : product_name,
            'star' : 4,
            'text' : 'Great'
        }
        url = reverse('reviews')
        client = api_client
        client._credentials = {
            'HTTP_AUTHORIZATION' : f'Bearer {access_token}'
        }
        response = client.post(url,data=data)
        assert response.status_code == 201
        assert response.json()['product'] == product_name

# Create your tests here.
