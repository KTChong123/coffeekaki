from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('products/', views.getProducts),
    path('product/<str:pk>', views.getProduct),
    path('order-items/', views.getOrderItems),
    path('order-item/<str:pk>', views.getOrderItem),
    path('create-order-item/', views.createOrderItem),
    path('update-order-item/<str:pk>', views.updateOrderItem),
    path('delete-order-item/<str:pk>', views.deleteOrderItem),

    path('orders/', views.getOrders),
    path('create-order/', views.createOrder),
]
