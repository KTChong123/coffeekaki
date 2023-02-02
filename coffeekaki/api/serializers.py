from rest_framework.serializers import ModelSerializer
from coffeekaki.models import *


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
