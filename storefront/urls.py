"""storefront URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from coffeekaki import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', views.loginPage_view, name="login"),
    path('logout/', views.logoutUser_view, name="logout"),
    path('register/', views.registerUser_view, name="register"),
    path("", include("allauth.urls")),  # most important

    path('', views.home_view, name="home"),
    path('products/<str:pk>/', views.products_view, name="products"),
    path('search/', views.search_view, name="search"),

    path('cart/', views.cart_view, name="cart"),
    path('checkout/', views.checkout_view, name="checkout"),
    path('update_item/', views.updateItem_view, name="update_item"),
    path('process_order/', views.processOrder_view, name="process_order"),

    path('update_order_item/', views.updateOrderItem_view,
         name="update_order_item"),
    path('order/<str:pk>/', views.order_view, name="order"),

    path('manage/', views.manage_view, name="manage"),
    path('manage/menu', views.manage_menu_view, name="manage_menu"),
    path('manage/menu/add-product/', views.add_product_view, name="add_product"),
    path('manage/menu/update-product/<str:pk>',
         views.update_product_view, name="update_product"),
    path('manage/menu/delete-product/<str:pk>',
         views.delete_product_view, name="delete_product"),

    path('stripe_checkout/', views.stripe_checkout_view, name="stripe_checkout"),
    path('success/', views.success_view, name="success"),
    path('cancel/', views.cancel_view, name="cancel"),

    path('stripe-card-payment/', views.stripe_card_payment_view,
         name="stripe_card_payment"),

    path('stripe-checkouts/', views.stripe_checkouts_view, name="stripe_checkouts"),
    path('create-payment-intent/', views.create_payment_intent_view,
         name="create_payment_intent"),
    path('payment-status/<str:pk>/',
         views.payment_status_view, name="payment_status"),

    path('table/<str:pk>/',
         views.table_view, name="table"),
    path('set-table-number/<str:pk>/',
         views.set_table_number_view, name="set_table_number"),

    path('api/', include('coffeekaki.api.urls'))
]
