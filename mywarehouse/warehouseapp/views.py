from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
from .forms import ReceiveProductForm, IssueProductForm


def receive_product(request):
    if request.method == 'POST':
        form = ReceiveProductForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            if quantity and price > 0:
                try:
                    product = Product.objects.get(name=product_name)
                    product.quantity += quantity
                    product.save()
                except Product.DoesNotExist:
                    Product.objects.create(name=product_name, quantity=quantity, price=price)

                return JsonResponse({
                    'status': 'success',
                    'message': 'Procuct received successfully',
                    'product': {
                    'name': product_name,
                    'quantity': quantity,
                    'price': price,
                }
                })
            else:
                return JsonResponse({'status': 'error', 'message':
                    'Quantity and price should be a positive value.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
    else:
        form = ReceiveProductForm()

    return render(request, 'receive_product.html', {'form': form})



def issue_product(request):
    products = Product.objects.all()
    status = None
    if request.method == 'POST':
        form = IssueProductForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            quantity = form.cleaned_data['quantity']
            if quantity > 0:
                try:
                    product = Product.objects.get(name=product_name)
                    if product.quantity >= quantity:
                        if product.quantity > quantity:
                            product.quantity -= quantity
                            product.save()
                        else:
                            product.delete()
                        total_cost = product.price * quantity
                        status  = {'status': 'success', 'message': f'{product_name} x {quantity} issued.'
                                                                             f' Total cost: {total_cost}$'}
                        return render(request, 'issue_status.html', {'status': status})
                    else:
                        status = {'status': 'error', 'message': 'Insufficient stock.'}
                except Product.DoesNotExist:
                    status = {'status': 'error', 'message': 'Product not found in inventory.'}
            else:
                status = {'status': 'error', 'message': 'Quantity should be a positive value'}
        else:
            status = {'status': 'error', 'message': 'Invalid request.'}
    else:
        form = IssueProductForm()
    return render(request, 'issue_product.html', {'form': form, 'products': products, 'status': status})




def display_product_list(request):
    products = Product.objects.all()
    if products:
        return render(request, 'product_list.html', {'products': products})
    else:
        return JsonResponse({'status': 'error', 'message': 'No products in inventory.'})
