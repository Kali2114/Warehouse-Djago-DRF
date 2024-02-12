from django.contrib.auth.views import LoginView
from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product, Company
from .views import ReceiveProductView, logout_user, IssueProductView, display_product_list, ProductDetails, \
    CompanyCreateView


class WarehouseTests(TestCase):

    def setUp(self):
        self.company = Company.objects.create(name='Makita')
        self.product = Product.objects.create(id=1, name='Testname', price=10, quantity=1,
                                              company=self.company)

#URL_TESTS

    def test_login_url(self):
        url = reverse('login')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.view_class, LoginView)

    def test_logout_url(self):
        url = reverse('logout')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func, logout_user)

    def test_receive_product_url(self):
        url = reverse('receive_product')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.view_class, ReceiveProductView)

    def test_issue_product_url(self):
        url = reverse('issue_product')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.view_class, IssueProductView)

    def test_display_product_list_url(self):
        url = reverse('display_product_list')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func, display_product_list)

    def test_product_detail_url(self):
        url = reverse('product_details', args=[self.product.id])
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.view_class, ProductDetails)

    def test_manage_companies_url(self):
        url = reverse('manage_companies')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.view_class, CompanyCreateView)

    def test_receive_product_api_url(self):
        url = reverse('receive-product-api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_issue_product_api_url(self):
        url = reverse('receive-product-api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_detal_view_api_url(self):
        url = reverse('receive-product-api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

#API_TESTS

    def test_receive_product_api(self):
        client = APIClient()
        url = reverse('receive-product-api')
        data = {
            'name': 'Test',
            'price': 10,
            'quantity': 1,
            'company': self.company.id
        }
        response = client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_issue_product_api(self):
        client = APIClient()
        url = reverse('issue-product-api')
        data = {
            'name': self.product.name,
            'quantity': 1
        }
        response = client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product_detail(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Testname')

#VIEWS_TESTS