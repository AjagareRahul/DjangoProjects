from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#CATEGORY
class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
         return self.name
     
''' working method:
Category    | Products
Electronics | 
Mobile, Laptop, TV
Clothing	| Shirt, Pant, Dress
Books	    | Novel, Textbook'''
     
     
     #PRODUCT TABLE
     
class Product(models.Model):
    Category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    price=models.FloatField()
    description=models.TextField()
    image=models.ImageField()
    stock=models.IntegerField()
    
    def __str__(self):
        return self.name
    #CART
class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Cart of {self.user.username}"
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.product.name}*{self.quantity}"
    
    
class Order(models.Model):
    STATUS_CHOICES=(('Pending','Pending'),('Shipped','Shipped'),('Delivered','Delivered'),('Cancelled','Cancelled'))
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_price=models.FloatField()
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    price=models.FloatField()
    def __str__(self):
        return f"{self.product.name}*{self.quantity} in Order #{self.order.id}"
    
class OrderAddress(models.Model):
    order=models.OneToOneField(Order,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    address=models.TextField(max_length=255)
    city=models.CharField(max_length=100)
    pincode=models.CharField(max_length=10)
    def __str__(self):
        return f"Address for Order #{self.order.id}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username


#WISHLIST
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    added_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate wishlist items
    
    def __str__(self):
        return f"{self.product.name} in {self.user.username}'s wishlist"
