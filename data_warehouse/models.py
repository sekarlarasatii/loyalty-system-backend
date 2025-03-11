from django.db import models

class TransactionDW(models.Model):
    transaction_id = models.CharField(max_length=255, unique=True)
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    points_used = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    failure_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"
