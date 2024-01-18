# views.py
from django.shortcuts import render
from .models import Discount

def discounted_products(request):
    # Get all discounted products
    discounted_items = Discount.objects.all()

    return render(request, 'discount_product.html', {'discounted_items': discounted_items})
