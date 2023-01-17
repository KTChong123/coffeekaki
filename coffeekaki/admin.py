from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(MenuCategorie)
admin.site.register(MenuType)
admin.site.register(MenuItem)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderUpdate)
admin.site.register(State)
