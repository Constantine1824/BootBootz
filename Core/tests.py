from django.test import TestCase
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Products
from .serializers import ProductsSerializer
import Core.signals
from Auth.models import AbstractUser,User
from urllib.parse import urlencode
from django.db.models import Q
import pytest

client = APIClient()


# class TestCoreView(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.serializer = ProductsSerializer
#         return super().setUp()

#     def testAllProductsView(self):
#         url = reverse('all')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code,status.HTTP_200_OK)

#     def testCreateAddressApiView(self):
#         pass

#     def testProductsRetrieveApiView(self):
#         product = Products.objects.get(id=2)
#         slug = product.slug
#         expected_response = self.serializer(product).data

#         url = reverse('ProductsRetrieveApiView',kwargs={'slug':slug})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code,status.HTTP_200_OK)
#         self.assertEqual(response.json(), expected_response)

#     def testSearchApiView(self):
        
#         q = 'Nike'
#         products_query = Products.objects.filter(
#                 Q(name__icontains=q)|
#                 Q(category__icontains=q)|
#                 Q(manufacturer__icontains=q)
#             )
#         serializer = self.serializer(products_query,many=True)
#         url = reverse('search')
#         query = {'q': 'Nike'}
#         full_url = '{}?{}'.format(url,urlencode(query))
#         print(full_url)
#         response = self.client.get(full_url)
#         self.assertEqual(response.status_code,status.HTTP_200_OK)
#         self.assertEqual(response.json(),serializer.data)

class TestProductsView:
    @pytest.mark.django_db(transaction=True)
    def test_all_products(self,products_obj):
        client = APIClient()
        products = products_obj
        serializer = ProductsSerializer(products,many=True)
        url = reverse('all')
        response = client.get(url)
        print(serializer.data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data
        assert len(serializer.data) >= 1

# Create your tests here.
