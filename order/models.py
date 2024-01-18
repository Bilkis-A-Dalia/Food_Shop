from django.db import models
from django.contrib.auth.models import User
from menu.models import FoodMenu
# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    food_items = models.ForeignKey(FoodMenu,on_delete=models.CASCADE,null=True,blank=True)
    total_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} {self.food_items.food_name}'
    
class  OrderHistry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    food_items = models.ForeignKey(FoodMenu,on_delete=models.CASCADE,null=True,blank=True)
    total_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} {self.food_items.food_name}'