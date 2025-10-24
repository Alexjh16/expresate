from django.urls import path
from .views import logoutUser, registrarUser, loginUser, api_loginUser

urlpatterns = [
    path('registrar/', registrarUser, name='registrarUser'),
    path('loginUser/', loginUser, name='loginUser'),
    path('logoutUser', logoutUser, name='logoutUser'),
    #send with a csrf token
    path('api/loginUser/', api_loginUser, name='api_login_user'),    
]