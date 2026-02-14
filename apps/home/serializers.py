# serializers.py
from rest_framework import serializers
from .models import Stock
class StockDataSerializer(serializers.Serializer):
    labels = serializers.ListField(child=serializers.CharField())
    series = serializers.ListField(child=serializers.ListField(child=serializers.FloatField()))

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['created_at', 'quantity', 'price']