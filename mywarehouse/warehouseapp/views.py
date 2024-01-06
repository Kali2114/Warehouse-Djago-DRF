from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from .models import Product
from .forms import ReceiveProductForm, IssueProductForm

@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

def logout_user(request):
    logout(request)
    return redirect('login')

class ReceiveProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ReceiveProductForm
    template_name = 'receive_product.html'

    def form_valid(self, form):
        product_name = form.cleaned_data['name']
        price = form.cleaned_data['price']
        quantity = form.cleaned_data['quantity']
        product, created = Product.objects.get_or_create(name=product_name,
                                                         defaults={'price': price, 'quantity': quantity})
        if price <= 0 or quantity <= 0:
            messages.error(self.request, 'Error. Price and quantity should be a positive value.')
            return render(self.request, 'receive_status.html')

        if not created:
            product.quantity += quantity

        product.save()

        messages.success(self.request, f'{quantity} x {product_name} received.')
        return render(self.request, 'receive_status.html')

class IssueProductView(LoginRequiredMixin, View):
    template_name = 'issue_product.html'

    def get(self, request):
        products = Product.objects.all()
        form = IssueProductForm()
        return render(request, self.template_name, {'products': products, 'form': form})

    def post(self, request):
        form = IssueProductForm(request.POST)

        if form.is_valid():
            product_name = form.cleaned_data['name']
            quantity = form.cleaned_data['quantity']
            if quantity > 0:
                try:
                    product = Product.objects.get(name=product_name)
                    if product.quantity >= quantity:
                        if product.quantity == quantity:
                            product.delete()
                        else:
                            product.quantity -= quantity
                            product.save()
                        messages.success(request, f'{quantity} x {product_name} issued.')
                    else:
                        messages.error(request, f'Insufficient stock.')
                except Product.DoesNotExist:
                    messages.error(request, f'Product {product_name} not found.')
            else:
                messages.error(request, 'Error. Quantity should be a positive value.')
        return render(self.request, 'issue_status.html')

@login_required
def display_product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


