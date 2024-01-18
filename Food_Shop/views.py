from django.shortcuts import render, get_object_or_404
from menu.models import FoodMenu
from category.models import Category

def Home(request, category_slug=None):
    data = FoodMenu.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        data = FoodMenu.objects.filter(category=category)
    category = Category.objects.all()
    return render(request, 'home.html', {'data': data, 'category': category})