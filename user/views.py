from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.utils.encoding import force_str
from order.models import Order,OrderHistry
from menu. models import FoodMenu
from django.db.models import Sum
from discount.models import Discount
from decimal import Decimal
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# from django.utils.text import force_text
from . import forms

def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f'https://flavorfusion-delights.onrender.com/user/active/{uid}/{token}/'
            email_subject = 'Confirm Your Email'
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})

            try:
                # send email
                email = EmailMultiAlternatives(email_subject, '', to=[user.email])
                email.attach_alternative(email_body, "text/html")
                email.send()
                messages.success(request, 'Account verification mail sent successfully')
                return redirect('register')
            except Exception as e:
                messages.error(request, f'Error sending verification email: {e}')
    else:
        register_form = forms.RegistrationForm()

    return render(request, 'register.html', {'form': register_form, 'type': 'Register'})


def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account successfully activated. You can now log in.')
        return redirect('register')
    else:
        messages.error(request, 'Invalid activation link. Please try again or contact support.')
        return redirect('register')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = forms.ChangeUserForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        profile_form = forms.ChangeUserForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': profile_form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            user_pass = form.cleaned_data['password']
            user = authenticate(username=user_name, password=user_pass)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('home')
        messages.warning(request, 'Login information incorrect')
        return render(request, 'login.html', {'form': form, 'type': 'Login'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'type': 'Login'})

def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required
def profile(request):
    user_details = User.objects.get(pk=request.user.pk)
    user = request.user
    orders = Order.objects.filter(user=user)
    total_cost = orders.aggregate(Sum('total_cost'))['total_cost__sum']
    return render(request, 'profile.html', {'user_details': user_details,'orders': orders, 'total_cost': total_cost})


@login_required
def add_to_cart(request, id):
    item = get_object_or_404(FoodMenu, pk=id)
    user = request.user
    discount_item = Discount.objects.filter(food_type=item).first()
    if discount_item:
        discount_decimal = Decimal(discount_item.discount) / 100
        total_cost = item.price - (item.price * discount_decimal)
    else:
        total_cost = item.price

    Order.objects.create(
        user=user,
        food_items = item,
        total_cost=total_cost,
    )

    return redirect('profile')

@login_required
def remove_from_cart(request, id):
    user = request.user
    order = get_object_or_404(Order, id=id)
    order.delete()
    return redirect('profile')

@login_required
def order(request, id):
    order = get_object_or_404(Order, id=id)
    user = request.user
    OrderHistry.objects.create(
        user=user,
        food_items = order.food_items,
        total_cost=order.total_cost,
    )
    order.delete()
    return redirect('orderhistory')

@login_required
def orderhistory(request):
    user = request.user

    # Retrieve all orders for the current user
    orderhistory = OrderHistry.objects.filter(user=user)
    total_cost = orderhistory.aggregate(Sum('total_cost'))['total_cost__sum']
    return render(request, 'order_history.html', {'orderhistory': orderhistory,'total_cost': total_cost})


# reservation 
@require_POST
def reservation(request):
    # Get form data
    name = request.POST.get('name')
    date = request.POST.get('date')
    request_details = request.POST.get('request')
    email = request.POST.get('email')
    no_of_people = request.POST.get('people')

    # Compose email message
    subject = f"Reservation Request from {name}"
    message_body = f"Name: {name}\nDate & Time: {date}\nSpecial Request: {request_details}\nEmail: {email}\nNo Of People: {no_of_people}"
    sender_email = email  # Using the email provided in the reservation form as the sender's email address
    recipient_email = ['bilkisadalia@gmail.com']  # Recipient's email address

    try:
        send_mail(subject, message_body, sender_email, recipient_email)
        # Email sent successfully
        return JsonResponse({'success': True})
    except Exception as e:
        # Error sending email
        return JsonResponse({'success': False, 'error_message': str(e)})