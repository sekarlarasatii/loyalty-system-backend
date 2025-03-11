from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer
from users.models import User
from data_warehouse.models import TransactionDW
from points.models import PointsConfiguration
from datetime import datetime

class SimulatePaymentView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        amount = request.data.get('amount')
        payment_method = request.data.get('payment_method')

        if payment_method == 'Points':
            if user.points_balance < amount:
                return Response({'detail': 'Insufficient points balance.'}, status=status.HTTP_400_BAD_REQUEST)
            user.points_balance -= amount
            points_used = amount
        else:
            points_used = 0

        # Simulate successful payment
        transaction = Transaction.objects.create(
            user=user,
            amount=amount,
            payment_method=payment_method,
            status='Success'
        )

        # Calculate earned points
        points_config = PointsConfiguration.objects.get(membership_status=user.membership_status)
        points_earned = (amount // points_config.threshold) * points_config.multiplier
        user.points_balance += points_earned
        user.save()

        # Create data warehouse record
        TransactionDW.objects.create(
            transaction_id=transaction.id,
            user_id=user.id,
            timestamp=datetime.now(),
            amount=amount,
            points_used=points_used,
            points_earned=points_earned,
            payment_method=payment_method,
            status='Success'
        )

        return Response({'detail': 'Payment simulated successfully.'}, status=status.HTTP_200_OK)
