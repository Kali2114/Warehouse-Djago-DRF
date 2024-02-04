from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView
from .models import Product, Company
from .forms import ReceiveProductForm, IssueProductForm, CompanyForm, CompanyDeleteForm


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
        company = form.cleaned_data['company']
        product, created = Product.objects.get_or_create(name=product_name,
                                                         defaults={'price': price, 'quantity': quantity,
                                                                   'company': company})
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

class CompanyCreateView(LoginRequiredMixin, View):
    template_name = 'manage_companies.html'

    def get(self, request):
        companies = Company.objects.all()
        form = CompanyForm()
        delete_form = CompanyDeleteForm()
        return render(request, self.template_name, {'companies': companies, 'form': form, 'delete_form': delete_form})

    def post(self, request):
        form = CompanyForm(request.POST)
        delete_form = CompanyDeleteForm(request.POST)

        if 'action' in request.POST and request.POST['action'] == 'create_company' and form.is_valid():
            company_name = form.cleaned_data['name']
            company = Company(name=company_name)
            company.save()

        elif 'action' in request.POST and request.POST['action'] == 'delete_company' and delete_form.is_valid():
            company_name_to_delete = delete_form.cleaned_data['name']
            company_to_delete = Company.objects.get(name=company_name_to_delete)
            company_to_delete.delete()


        companies = Company.objects.all()
        return render(request, self.template_name, {'companies': companies, 'form': form, 'delete_form': delete_form})
class ProductDetail(LoginRequiredMixin, View):
    pass

@login_required
def display_product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


