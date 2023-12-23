from django.urls import path
from . import views

urlpatterns = [
    path('receive_product/', views.receive_product, name='receive_product'),
    path('issue_product/', views.issue_product, name='issue_product'),
    path('display_product_list/', views.display_product_list),
]