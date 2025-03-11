import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.mark.django_db
def test_user_registration(api_client):
    url = reverse('user-register')
    data = {
        'email': 'testuser@example.com',
        'name': 'Test User',
        'password': 'testpassword123',
        'password2': 'testpassword123'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_user_login(api_client, create_user):
    user = create_user(email='testuser@example.com', password='testpassword123', name='Test User')
    url = reverse('user-login')
    data = {
        'email': 'testuser@example.com',
        'password': 'testpassword123'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_user_profile(api_client, create_user):
    user = create_user(email='testuser@example.com', password='testpassword123', name='Test User')
    url = reverse('user-profile')
    api_client.force_authenticate(user=user)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == 'testuser@example.com'
    assert response.data['name'] == 'Test User'

@pytest.mark.django_db
def test_password_reset(api_client, create_user):
    user = create_user(email='testuser@example.com', password='testpassword123', name='Test User')
    url = reverse('password-reset')
    data = {
        'email': 'testuser@example.com'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert 'detail' in response.data
