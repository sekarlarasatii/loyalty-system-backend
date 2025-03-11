from django.db import models
from users.models import User

class PointsConfiguration(models.Model):
    membership_status = models.CharField(
        max_length=10,
        choices=[('Bronze', 'Bronze'), ('Silver', 'Silver'), ('Gold', 'Gold')]
    )
    multiplier = models.FloatField()
    threshold = models.IntegerField()

    def __str__(self):
        return f"{self.membership_status} - Multiplier: {self.multiplier}, Threshold: {self.threshold}"

class Voucher(models.Model):
    description = models.TextField()
    points_required = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

class PointsTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('Earn', 'Earn'),
        ('Redeem', 'Redeem')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    points = models.IntegerField()
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} - {self.points} points"
