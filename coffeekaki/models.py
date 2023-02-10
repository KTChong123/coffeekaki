from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.


class MenuCategorie(models.Model):
    categories = models.CharField(max_length=200)

    def __str__(self):
        return self.categories


class MenuType(models.Model):
    category = models.ForeignKey(
        MenuCategorie, on_delete=models.CASCADE)
    menu_type = models.CharField(max_length=300)

    def __str__(self):
        return self.menu_type


class MenuItem(models.Model):
    menu_type = models.ForeignKey(MenuType, on_delete=models.CASCADE)
    menu_item = models.CharField(max_length=300)
    description = models.CharField(null=True, blank=True, max_length=300)
    price = models.FloatField(max_length=300)
    photo = models.CharField(null=True, blank=True, max_length=300)

    def __str__(self):
        return self.menu_item


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(
        upload_to='static/products')
    category = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    number_of_sales = models.IntegerField(default=0)

    class Meta:
        ordering = ['-number_of_sales', 'category', 'type']

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    class Meta:
        ordering = ['-date_ordered']

    def __str__(self):
        title = str(self.customer) + " " + str(self.date_ordered)
        return title

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    table_number = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        title = str(self.id) + " " + str(self.order) + " " + str(self.product) + \
            " (Complete: " + str(self.complete) + ")"
        return title

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class OrderUpdate(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.timestamp)


class State(models.Model):
    name = models.CharField(max_length=200, null=True)
    state = models.BooleanField(default=False)

    def __str__(self):
        title = str(self.id) + " " + str(self.name)
        return title
