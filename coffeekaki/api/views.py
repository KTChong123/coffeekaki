from rest_framework.decorators import api_view
from rest_framework.response import Response
from coffeekaki.models import *
from .serializers import *


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/products',
        'GET /api/products/:id',
        'GET /api/orders',
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
def getOrders(request):
    orders = OrderItem.objects.all()
    serializer = OrderItemSerializer(orders, many=True)
    return Response(serializer.data)
