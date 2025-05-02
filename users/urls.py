from django.urls import path
from .views import logoutUser, registrarUser, loginUser

urlpatterns = [
    path('registrar/', registrarUser, name='registrarUser'),
    path('loginUser/', loginUser, name='loginUser'),
    path('cerrar/session/', logoutUser, name='logout.session'),
]