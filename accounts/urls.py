from xml.etree.ElementInclude import include
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('product/', views.product, name="product"),
    path('customer/<str:customerId>', views.customer, name="customer"),
    path('create-order/<str:custId>', views.createOrder, name="create_order"),
    path('update-order/<str:orderId>', views.updateOrder, name="update_order"),
    path('delete-order/<str:orderId>', views.deleteOrder, name="delete_order"),
    path('update-customer/<str:custId>',
         views.updateCustomer, name="update_customer"),
    path('delete-customer/<str:custId>',
         views.deleteCustomer, name='delete_customer'),
    path('create-customer/', views.createCustomer, name='create_customer'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout')

]
