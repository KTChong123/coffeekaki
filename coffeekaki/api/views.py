from rest_framework.decorators import api_view
from rest_framework.response import Response
from coffeekaki.models import *
from .serializers import *
from rest_framework import status
import json


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/products',
        'GET /api/product/:id',
        'GET /api/order-items',
        'GET /api/order-item/:id',
        'POST /api/create-order-item',
        'POST /api/update-order-item/:id',
        'DELETE /api/deleteß-order-item/:id',
        'GET /api/orders',
        'POST /api/create-order',
    ]
    return Response(routes)


@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getOrderItems(request):
    orders = OrderItem.objects.all()
    serializer = OrderItemSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getOrderItem(request, pk):
    orderItem = OrderItem.objects.get(id=pk)
    serializer = OrderItemSerializer(orderItem, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createOrderItem(request):
    serializer = OrderItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def updateOrderItem(request, pk):
    orderItem = OrderItem.objects.get(id=pk)
    serializer = OrderItemSerializer(instance=orderItem, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteOrderItem(request, pk):
    orderItem = OrderItem.objects.get(id=pk)
    orderItem.delete()

    return Response('Order item deleted')


@api_view(['GET'])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createOrder(request):
    serializer = OrderSerializer(data=request.data)

    print(serializer)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()

    return Response('Order deleted')
