from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=11)
    adres = models.TextField()

    def __str__(self):
        return self.user.username + "'s Profile"
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RestaurantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/restaurant')
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    categories = models.ManyToManyField(ProductCategory, related_name="restaurants")

    def __str__(self):
        return self.name + "'s Profile"


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='images/product')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# class Order(models.Model):
#     user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, null=False)
#     restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, null=True)
#     order_date = models.DateTimeField(auto_now_add=True)
#     is_cancelled = models.BooleanField(default=False)
#     order_note = models.TextField(max_length=150, blank=True, null=True)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False)

#     def __str__(self):
#         return f"{self.user.user}'s order to {self.restaurant.name} restaurant"

#     def get_total_price(self):
#         total = sum(item.product.price * item.quantity for item in self.order_items.all())
#         return total

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     additional_notes = models.TextField(max_length=150, blank=True, null=True)

#     def __str__(self):
#         return f"{self.quantity}x {self.product.name} for {self.order.user}"


    
    
class OrderUser(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    adress = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
   
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    order_user = models.ForeignKey(OrderUser, on_delete=models.CASCADE, null=True)
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)
    order_note = models.TextField(max_length=150, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False)

    def __str__(self):
        return f"{self.user}'s order to {self.restaurant.name} restaurant"

    def get_total_price(self):
        total = sum(item.product.price * item.quantity for item in self.order_items.all())
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    additional_notes = models.TextField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} for {self.order.user}"