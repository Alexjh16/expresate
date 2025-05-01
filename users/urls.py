from django.urls import path
from .views import registrarUser, loginUser

urlpatterns = [
    path('registrar/', registrarUser, name='registrarUser'),
    path('loginUser', loginUser, name='loginUser'),
]