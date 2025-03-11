from rest_framework import serializers
from .models import PointsConfiguration, Voucher, PointsTransaction

class PointsConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsConfiguration
        fields = '__all__'

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'

class PointsTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsTransaction
        fields = '__all__'
