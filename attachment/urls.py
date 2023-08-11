from django.urls import path
from .views import *
from django.conf import settings

urlpatterns = [
       ## authentication paths
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logbook/', update_logbook, name = 'update_logbook'),
]