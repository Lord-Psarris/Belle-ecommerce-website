from django.db import models
from accounts.models import Users


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255, default='')
    in_stock = models.PositiveIntegerField(default=0)
    colors_available = models.CharField(max_length=255, default='')
    sizes_available = models.CharField(max_length=255, default='')

    description = models.TextField(default='')
    has_discount = models.BooleanField(default='')
    discounted_percent = models.PositiveIntegerField(default=0)
    is_new = models.BooleanField(default=True)

    price = models.PositiveIntegerField(default=0)
    sales_count = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=255, default='clothing')

    def __str__(self):
        return self.name

    def get_short_name(self):
        return self.name.lower().replace(' ', '')


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.FileField()

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=5, default='')
    color = models.CharField(max_length=255, default='')

    def __str__(self):
        return f'{self.user} - {self.product}'


class Wishlist(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.product}'


class Orders(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')
    post_code = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=255, default='')
    order_notes = models.TextField(default='')
    total_price = models.CharField(max_length=255, default='')
    status = models.CharField(max_length=255, default='pending')

    def __str__(self):
        return self.user.email


class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order.user.email}: Order-{self.order.id}'

