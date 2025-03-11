import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from transactions.models import Transaction
from data_warehouse.models import TransactionDW

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def authenticate_user(api_client, create_user):
    def make_authentication(user_data):
        user = create_user(**user_data)
        response = api_client.post(reverse('token_obtain_pair'), user_data)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        return user
    return make_authentication

@pytest.mark.django_db
def test_simulate_payment_with_points(api_client, authenticate_user):
    user_data = {'email': 'testuser@example.com', 'password': 'testpassword', 'name': 'Test User'}
    user = authenticate_user(user_data)
    user.points_balance = 1000
    user.save()

    url = reverse('simulate-payment')
    data = {'amount': 500, 'payment_method': 'Points'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['detail'] == 'Payment simulated successfully.'

    user.refresh_from_db()
    assert user.points_balance == 500

    transaction = Transaction.objects.get(user=user)
    assert transaction.amount == 500
    assert transaction.payment_method == 'Points'
    assert transaction.status == 'Success'

    transaction_dw = TransactionDW.objects.get(transaction_id=transaction.id)
    assert transaction_dw.amount == 500
    assert transaction_dw.points_used == 500
    assert transaction_dw.points_earned == 0
    assert transaction_dw.payment_method == 'Points'
    assert transaction_dw.status == 'Success'

@pytest.mark.django_db
def test_simulate_payment_with_dummy_virtual_account(api_client, authenticate_user):
    user_data = {'email': 'testuser@example.com', 'password': 'testpassword', 'name': 'Test User'}
    user = authenticate_user(user_data)

    url = reverse('simulate-payment')
    data = {'amount': 1000, 'payment_method': 'Dummy Virtual Account'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['detail'] == 'Payment simulated successfully.'

    user.refresh_from_db()
    assert user.points_balance == 0

    transaction = Transaction.objects.get(user=user)
    assert transaction.amount == 1000
    assert transaction.payment_method == 'Dummy Virtual Account'
    assert transaction.status == 'Success'

    transaction_dw = TransactionDW.objects.get(transaction_id=transaction.id)
    assert transaction_dw.amount == 1000
    assert transaction_dw.points_used == 0
    assert transaction_dw.points_earned == 0
    assert transaction_dw.payment_method == 'Dummy Virtual Account'
    assert transaction_dw.status == 'Success'
