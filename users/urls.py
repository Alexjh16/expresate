from django.urls import path
from .views import logoutUser, registrarUser, loginUser

urlpatterns = [
    path('registrar/', registrarUser, name='registrarUser'),
    path('loginUser/', loginUser, name='loginUser'),
    path('logoutUser', logoutUser, name='logoutUser'),
]