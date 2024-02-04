from rest_framework import serializers
from .models import Product, Company

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
#             raise serializers.ValidationError("Price and quantity should be a positive values.")
#         return data
# class CompanySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company
#         fields = '__all__'

class ReceiveProductSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    class Meta:
        model = Product
        fields = '__all__'

    def validate_name(self, value):
        return value.title().strip()

    def validate(self, data):
        if data['price'] <= 0 or data['quantity'] <= 0:
            raise serializers.ValidationError("Price and quantity should be a positive values.")
        return data
#
class IssueProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(read_only=True)
    company = serializers.CharField(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity', 'company']

    def validate_name(self, value):
        return value.title().strip()

    def validate(self, data):
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity should be positive value.")
        return data
