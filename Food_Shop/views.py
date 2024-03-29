from django.shortcuts import render, get_object_or_404
from menu.models import FoodMenu,Review
from category.models import Category

def Home(request, category_slug=None):
    data = FoodMenu.objects.all()
    reviews = Review.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        data = FoodMenu.objects.filter(category=category)
    category = Category.objects.all()
    return render(request, 'home.html', {'data': data, 'category': category,'reviews': reviews})

def Service(request):
    return render(request, 'service.html')
def ContactUs(request):
    return render(request, 'about_us.html')