# views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import FoodMenu, Review
from order.models import OrderHistry
from .forms import ReviewForm

class AddReviewView(View):
    template_name = 'add_review.html'

    def get(self, request, id):
        food = FoodMenu.objects.get(pk=id)
        if OrderHistry.objects.filter(user=request.user, food_items=food).exists():
            form = ReviewForm()
            return render(request, self.template_name, {'food': food, 'form': form})
        else:
            messages.error(request, 'You can only review items you have ordered.')
            return redirect('detail_food', id=id)

    def post(self, request,id):
        food = FoodMenu.objects.get(pk=id)
        form = ReviewForm(request.POST)
        if not OrderHistry.objects.filter(user=request.user, food_items=food).exists():
            messages.error(request, 'You can only review items you have ordered.')
            return redirect('detail_food', id=id)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.food = food
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('orderhistory')
        else:
            messages.error(request, 'Invalid review. Please check your input.')

        return render(request, self.template_name, {'food': food, 'form': form})
