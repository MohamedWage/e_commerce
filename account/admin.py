from django.contrib import admin
from .models import User, UserRole, Category, Product, Order, OrderItem


# Register your models here.


admin.site.register(UserRole)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)