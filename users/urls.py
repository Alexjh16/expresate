from django.urls import path
from .views import registrarUser, altcha_challenge

urlpatterns = [
    path('registrar/', registrarUser, name='registrarUser'),
]