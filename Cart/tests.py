from django.test import TestCase
import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_unauthorized_request(api_client):
    url = reverse('cart details')
    response = api_client.get(url)
    assert response.status_code == 401
# Create your tests here.
