from rest_framework import serializers
from .models import Product

class BaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_name(self, value):
        return value.title().strip()

    def validate(self, data):
        if data['price'] <= 0 or data['quantity'] <= 0:
            raise serializers.ValidationError("Price and quantity should be positive values.")
        return data


class ReceiveProductSerializer(BaseProductSerializer):
    class Meta(BaseProductSerializer.Meta):
        pass

class IssueProductSerializer(BaseProductSerializer):
    price = serializers.FloatField(required=False, default=None, allow_null=True)
    class Meta(BaseProductSerializer.Meta):
        fields = ['name', 'quantity', 'price']

