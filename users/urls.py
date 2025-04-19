from django.urls import path
from .views import registrarUser

urlpatterns = [
    path('registrar/', registrarUser, name='registrarUser'),
]