from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
from points.models import PointsTransaction

@shared_task
def expire_points():
    one_year_ago = timezone.now() - timedelta(days=365)
    expired_transactions = PointsTransaction.objects.filter(timestamp__lte=one_year_ago, transaction_type='Earn')
    for transaction in expired_transactions:
        transaction.points = 0
        transaction.save()
