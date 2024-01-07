from rest_framework import serializers
from .models import Product

# class BaseProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'
#
#     def validate_name(self, value):
#         return value.title().strip()
#
#     def validate(self, data):
#         if data['price'] <= 0 or data['quantity'] <= 0:
#             raise serializers.ValidationError("Price and quantity should be positive values.")
#         return data

#
class ReceiveProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_name(self, value):
        return value.title().strip()

    def validate(self, data):
        if data['price'] <= 0 or data['quantity'] <= 0:
            raise serializers.ValidationError("Price and quantity should be positive values.")
        return data
#
class IssueProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(read_only=True)
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity']

    def validate_name(self, value):
        return value.title().strip()

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity should be positive value.")
        return data





