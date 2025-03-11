from django.db import models
from users.models import User

class Transaction(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Points', 'Points'),
        ('Dummy Virtual Account', 'Dummy Virtual Account'),
        ('Dummy Credit Card', 'Dummy Credit Card')
    ]

    STATUS_CHOICES = [
        ('Success', 'Success'),
        ('Failed', 'Failed')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    failure_reason = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.amount} - {self.payment_method} - {self.status}"
