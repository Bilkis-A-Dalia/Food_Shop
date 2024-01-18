from django.db import models
from category.models import Category
from django.contrib.auth.models import User

# Create your models here.

STAR_CHOICES =[
    ('★','★'),
    ('★★','★★'),
    ('★★★','★★★'),
    ('★★★★','★★★★'),
    ('★★★★★','★★★★★')
]  
class FoodMenu(models.Model):
    food_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu/media/uploads')
    category = models.ManyToManyField(Category)
    price = models.DecimalField(max_digits=20,decimal_places = 2)

    def __str__(self):
        return self.food_name


class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    food=models.ForeignKey(FoodMenu,on_delete=models.CASCADE,related_name='reviews')
    review=models.TextField()
    review_date=models.DateField(auto_now_add=True)
    rating = models.CharField(choices = STAR_CHOICES,max_length=10,blank= True,null = True)
     
    def __str__(self) -> str:
        return f'{self.user.username}-{self.food.food_name}'