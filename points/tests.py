import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import PointsConfiguration, Voucher, PointsTransaction
from users.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def create_admin_user(db):
    def make_admin_user(**kwargs):
        return User.objects.create_superuser(**kwargs)
    return make_admin_user

@pytest.fixture
def create_points_configuration(db):
    def make_points_configuration(**kwargs):
        return PointsConfiguration.objects.create(**kwargs)
    return make_points_configuration

@pytest.fixture
def create_voucher(db):
    def make_voucher(**kwargs):
        return Voucher.objects.create(**kwargs)
    return make_voucher

@pytest.mark.django_db
def test_points_configuration_list_create(api_client, create_admin_user):
    admin_user = create_admin_user(email='admin@example.com', password='adminpassword')
    api_client.force_authenticate(user=admin_user)

    url = reverse('points-configuration')
    data = {
        'membership_status': 'Bronze',
        'multiplier': 1.0,
        'threshold': 10000
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert PointsConfiguration.objects.count() == 1

@pytest.mark.django_db
def test_voucher_list_create(api_client, create_admin_user):
    admin_user = create_admin_user(email='admin@example.com', password='adminpassword')
    api_client.force_authenticate(user=admin_user)

    url = reverse('vouchers')
    data = {
        'description': '10% Discount Voucher',
        'points_required': 100,
        'is_active': True
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Voucher.objects.count() == 1

@pytest.mark.django_db
def test_redeem_voucher(api_client, create_user, create_voucher):
    user = create_user(email='user@example.com', password='password', points_balance=200)
    api_client.force_authenticate(user=user)

    voucher = create_voucher(description='10% Discount Voucher', points_required=100, is_active=True)
    url = reverse('redeem-voucher', kwargs={'voucher_id': voucher.id})

    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert PointsTransaction.objects.count() == 1
    user.refresh_from_db()
    assert user.points_balance == 100

@pytest.mark.django_db
def test_points_transaction_history(api_client, create_user, create_points_configuration):
    user = create_user(email='user@example.com', password='password')
    api_client.force_authenticate(user=user)

    PointsTransaction.objects.create(
        user=user,
        transaction_type='Earn',
        points=10,
        description='Test transaction'
    )

    url = reverse('points-transaction-history')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
