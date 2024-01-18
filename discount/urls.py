# urls.py
from django.urls import path
from .views import discounted_products

urlpatterns = [
    path('discounted_products/', discounted_products, name='discounted_products'),
]