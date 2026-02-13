from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, second_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            second_name=second_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, second_name, password=None, **extra_fields):
        admin_role, _ = UserRole.objects.get_or_create(name='Admin')
        extra_fields.setdefault('user_role', admin_role)
        
        user = self.create_user(email, first_name, second_name, password, **extra_fields)
        user.save(using=self._db)
        return user

class UserRole(models.Model):
    name = models.CharField(max_length=50)
 
    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    objects = MyUserManager()
    email = models.EmailField(unique=True,max_length=255,)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    user_role = models.ForeignKey(UserRole,related_name='role', on_delete=models.CASCADE,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined =models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'second_name']
    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        if self.user_role and self.user_role.name == 'Admin':
            return True
        return False

    def has_perm(self, perm, obj=None):
        return self.is_staff
    
    def has_module_perms(self, app_label):
        return self.is_staff


    
class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1024)
    Category = models.ForeignKey(Category,related_name="category",on_delete=models.CASCADE)
    # user = models.ForeignKey(User,related_name="user",on_delete=models.CASCADE)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    Purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    disscount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    quantity = models.IntegerField()
    def __str__(self):
        return self.name
    



class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    address = models.TextField()
    def __str__(self):
        return f"Order {self.id} by {self.user.email}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='orderItems',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='product',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
