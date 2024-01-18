from django.db import models
from menu.models import FoodMenu
# Create your models here.
class Discount(models.Model):
    food_type = models.OneToOneField(FoodMenu,on_delete = models.CASCADE)
    discount = models.IntegerField()

    def __str__(self):
        return f'{self.food_type.food_name} {self.discount}'