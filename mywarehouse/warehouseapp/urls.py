from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('index/', views.index, name='index'),
    path('receive_product/', views.ReceiveProductView.as_view(), name='receive_product'),
    path('issue_product/', views.IssueProductView.as_view(), name='issue_product'),
    path('display_product_list/', views.display_product_list, name='display_product_list'),
]