
from django.contrib import admin
from  .import views
from django.urls import path,include


urlpatterns = [
    path('register/',views.register,name = 'register'),
    path('profile/',views.profile,name='profile'),
    path('profile/edit',views.edit_profile,name = 'edit_profile'),
    path('login/',views.user_login,name = 'user_login'),
    path('logout/',views.user_logout,name = 'user_logout'),
    path('active/<uid64>/<token>/', views.activate,name = 'activate'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/<int:id>/', views.order, name='order'),
    path('orderhistory/',views.orderhistory,name='orderhistory'),
    path('reservation/',views.reservation,name='reservation'),
    path('pass_change/',views.pass_change,name='pass_change'), 
    path('reset_pass/',views.reset_pass,name='reset_pass'),
    path('set_pass/<uid64>/<token>',views.set_pass,name='set_pass'),
]

