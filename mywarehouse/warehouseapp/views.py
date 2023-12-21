from django.shortcuts import render
from django.http import JsonResponse
from models import Product

def receive_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        if quantity and price > 0:
            try:
                product = Product.objects.get(name=product_name)
                product.quantity += quantity
                product.save()
            except Product.DoesNotExist:
                Product.object.create(name=product_name, quantity=quantity, price=price)

            return JsonResponse({
                'status': 'success',
                'message': 'Procuct received successfully',
                'product': {
                'name': product_name,
                'quantity': quantity,
                'price': price
            }
            })
        else:
            return JsonResponse({'status': 'error', 'message':
                'Quantity and price should be a positive value.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request.'})



def issue_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity')
    if quantity > 0:
        try:
            product = Product.objects.get(name=product_name)
            if product.quantity >= quantity:
                if product.quantity > quantity:
                    product.quantity -= quantity
                    product.save()
                else:
                    product.delete()
                return JsonResponse({'status': 'success', 'message': f'{product_name} x {quantity} issued.'})
        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found in inventory.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request.'})



def display_product_list(request):
    products = Product.objects.all()
    if products:
        return render(request, 'product_list.html', {'products': products})
    else:
        return JsonResponse({'status': 'error', 'message': 'No products in inventory.'})
