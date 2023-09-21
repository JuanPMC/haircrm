from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home),
    path('signup/',views.signup),
    path('signin/',views.signin),
    path('signout/',views.signout),
]
