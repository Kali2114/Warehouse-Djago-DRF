from rest_framework import generics, status
from rest_framework.response import Response
from .models import Product
from .serializers import ReceiveProductSerializer, IssueProductSerializer

class ReceiveProductViewApi(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ReceiveProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_name = serializer.validated_data['name']
        quantity = serializer.validated_data['quantity']
        price = serializer.validated_data['price']

        product, created = Product.objects.get_or_create(name=product_name,

                                                         defaults={'price': price, 'quantity': quantity})
        # if quantity <= 0 or price <= 0:
        #     return Response({'error': 'Quantity and price should be a positive value.'},
        #                     status=status.HTTP_400_BAD_REQUEST)

        if not created:
            product.quantity += quantity
            product.save()
            return Response({'message': f'{product_name.title().strip()} x {quantity} received.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': f'Added new product: {product_name.title().strip()} x {quantity}'},
                            status=status.HTTP_201_CREATED)

class IssueProductViewApi(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = IssueProductSerializer
    lookup_field = 'name'
    lookup_url_kwarg = 'name'

    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = IssueProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_update(self, serializer):
        product_name = self.kwargs['name']
        quantity = serializer.validated_data['quantity']

        try:
            product = Product.objects.get(name=product_name)
            if product.quantity >= quantity:
                if product.quantity > quantity:
                    product.quantity -= quantity
                    product.save()
                else:
                    product.delete()
                return Response({'message': f'{quantity} x {product_name} issued.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Insufficient stock.'}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'error': f'Product {product_name} not found.'}, status=status.HTTP_404_NOT_FOUND)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ReceiveProductSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        quantity_to_issue = self.request.data.get('quantity')

        # if quantity_to_issue <= 0:
        #     return Response({'error': 'Quantity should be a positive value.'}, status=status.HTTP_400_BAD_REQUEST)

        if instance.quantity >= quantity_to_issue:
            instance.quantity -= quantity_to_issue

            if instance.quantity == 0:
                instance.delete()
                return Response({'message': f'Product {instance.name} fully issued.'}, status=status.HTTP_200_OK)
            else:
                instance.save()
                return Response({'message': f'{quantity_to_issue} x {instance.name} issued.'},
                                status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Insufficient stock.'}, status=status.HTTP_400_BAD_REQUEST)