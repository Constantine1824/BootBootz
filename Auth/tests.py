from django.test import TestCase
import pytest
from django.urls import reverse
from .serializers import UserSerializer
from rest_framework.test import APIClient

class TestAuth:
    
    @pytest.mark.django_db
    def test_signup(self,api_client):
        """This tests the signup endpoint"""
        data = {
            'username':'aetaiwo',
            'password' : 'Constant',
            'email' : 'ayomidet905@gmail.com',
            'password2' : 'Constant',
            'first_name' : 'Ayomide',
            'last_name' : 'Taiwo',
            'is_verified' : False
        }
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        url = reverse('signup')
        response = api_client.post(url,data=data)
        assert response.status_code == 201
        assert response.json() == serializer.data
    
    @pytest.mark.django_db
    def test_login(self,api_client,create_user):
        """This will test both the login endpoint and the refresh endpoint"""
        url = reverse('login')
        # access the endpoint for the refresh token
        ref_url = reverse('refresh')
        user = create_user(username='aetaiwo',password='Constant')
        data = {
            'username' :'aetaiwo',
            'password' : 'Constant'
        }
        response = api_client.post(url,data=data)
        refresh_token = {
            'refresh':response.json()['refresh']
            }
        refresh_response = api_client.post(ref_url,data=refresh_token)
        assert response.status_code == 200
        assert refresh_response.status_code == 200
        assert 'access' in refresh_response.json()
        assert 'access' in response.json()
        assert 'refresh' in response.json()
    
    @pytest.mark.django_db
    def test_email_sending(self,api_client,get_token):
        url = reverse('send mail')
        response = api_client
        response._credentials = {
            'HTTP_AUTHORIZATION' : f'Bearer {get_token}'
        }
        print(response._credentials)
        response = response.get(url)
        print(api_client.credentials())
        print(response.json())
        assert response.status_code == 200
        assert response.json()['detail'] == 'email sent'


# Create your tests here.
