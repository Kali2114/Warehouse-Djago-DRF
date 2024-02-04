from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Product
from .serializers import IssueProductSerializer, ReceiveProductSerializer


class ReceiveProductViewApi(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ReceiveProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_name = serializer.validated_data['name']
        quantity = serializer.validated_data['quantity']
        price = serializer.validated_data['price']
        company = serializer.validated_data['company']

        product, created = Product.objects.get_or_create(name=product_name,
                                                         defaults={'price': price, 'quantity': quantity,
                                                                   'company': company})

        if not created:
            product.quantity += quantity
            product.save()
            return Response({'message': f'{product_name.title().strip()} x {quantity} received.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': f'Added new product: {product_name.title().strip()} x {quantity}'},
                            status=status.HTTP_201_CREATED)

class IssueProductViewApi(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = IssueProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_name = serializer.validated_data['name']
        quantity_to_issue = serializer.validated_data['quantity']
        product = get_object_or_404(Product, name=product_name)

        if product.quantity >= quantity_to_issue > 0:
            if product.quantity == quantity_to_issue:
                product.delete()
            else:
                product.quantity -= quantity_to_issue
                product.save()
            return Response({'message': f'{quantity_to_issue} x {product_name} issued. Total cost: '
                                        f'{product.price * quantity_to_issue}$.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid quantity or insufficient stock.'},
                            status=status.HTTP_400_BAD_REQUEST)

class ProductDetailViewApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ReceiveProductSerializer
