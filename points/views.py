from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PointsConfiguration, Voucher, PointsTransaction
from .serializers import PointsConfigurationSerializer, VoucherSerializer, PointsTransactionSerializer
from users.models import User

class PointsConfigurationListCreateView(generics.ListCreateAPIView):
    queryset = PointsConfiguration.objects.all()
    serializer_class = PointsConfigurationSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return super().get_permissions()

class VoucherListCreateView(generics.ListCreateAPIView):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return super().get_permissions()

class PointsTransactionListView(generics.ListAPIView):
    serializer_class = PointsTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PointsTransaction.objects.filter(user=user)

class RedeemVoucherView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, voucher_id):
        user = request.user
        try:
            voucher = Voucher.objects.get(id=voucher_id, is_active=True)
        except Voucher.DoesNotExist:
            return Response({"error": "Voucher not found or inactive"}, status=status.HTTP_404_NOT_FOUND)

        if user.points_balance < voucher.points_required:
            return Response({"error": "Insufficient points"}, status=status.HTTP_400_BAD_REQUEST)

        user.points_balance -= voucher.points_required
        user.save()

        PointsTransaction.objects.create(
            user=user,
            transaction_type='Redeem',
            points=-voucher.points_required,
            description=f"Redeemed {voucher.description}"
        )

        return Response({"message": "Voucher redeemed successfully"}, status=status.HTTP_200_OK)

def calculate_earned_points(transaction_amount, membership_status):
    try:
        config = PointsConfiguration.objects.get(membership_status=membership_status)
    except PointsConfiguration.DoesNotExist:
        return 0

    points = (transaction_amount // config.threshold) * config.multiplier
    return points
