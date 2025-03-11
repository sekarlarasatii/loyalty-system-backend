import pytest
from django.utils import timezone
from data_warehouse.models import TransactionDW
from users.models import User

@pytest.mark.django_db
def test_create_transaction_dw():
    user = User.objects.create_user(email='testuser@example.com', password='testpassword')
    transaction = TransactionDW.objects.create(
        transaction_id='12345',
        user_id=user,
        amount=10000,
        points_used=100,
        points_earned=10,
        payment_method='Dummy Credit Card',
        status='Success',
        failure_reason=''
    )
    assert transaction.transaction_id == '12345'
    assert transaction.user_id == user
    assert transaction.amount == 10000
    assert transaction.points_used == 100
    assert transaction.points_earned == 10
    assert transaction.payment_method == 'Dummy Credit Card'
    assert transaction.status == 'Success'
    assert transaction.failure_reason == ''

@pytest.mark.django_db
def test_transaction_dw_failure():
    user = User.objects.create_user(email='testuser2@example.com', password='testpassword')
    transaction = TransactionDW.objects.create(
        transaction_id='67890',
        user_id=user,
        amount=5000,
        points_used=50,
        points_earned=5,
        payment_method='Dummy Virtual Account',
        status='Failed',
        failure_reason='Insufficient funds'
    )
    assert transaction.transaction_id == '67890'
    assert transaction.user_id == user
    assert transaction.amount == 5000
    assert transaction.points_used == 50
    assert transaction.points_earned == 5
    assert transaction.payment_method == 'Dummy Virtual Account'
    assert transaction.status == 'Failed'
    assert transaction.failure_reason == 'Insufficient funds'
