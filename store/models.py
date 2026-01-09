from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='food/',null=True,blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id}"        

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.food_item.name} x {self.quantity}"        
