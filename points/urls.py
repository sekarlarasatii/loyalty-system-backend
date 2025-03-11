from django.urls import path
from .views import (
    PointsConfigurationView,
    VoucherView,
    PointsTransactionView,
    RedeemVoucherView,
    PointsTransactionHistoryView,
)

urlpatterns = [
    path('points-configuration/', PointsConfigurationView.as_view(), name='points-configuration'),
    path('vouchers/', VoucherView.as_view(), name='vouchers'),
    path('points-transactions/', PointsTransactionView.as_view(), name='points-transactions'),
    path('redeem-voucher/', RedeemVoucherView.as_view(), name='redeem-voucher'),
    path('points-transaction-history/', PointsTransactionHistoryView.as_view(), name='points-transaction-history'),
]
