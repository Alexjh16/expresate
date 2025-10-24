from . views import get_nearby_treasures, create_treasure, claim_treasure, get_user_treasures, get_user_stats
from django.urls import path
urlpatterns = [
    path('treasures/nearby/', get_nearby_treasures, name='get_nearby_treasures'),
    path('treasures/create/', create_treasure, name='create_treasure'),
    path('treasures/<str:id>/claim/', claim_treasure, name='claim_treasure'),  # Cambiado a <str:id> para aceptar ObjectId de MongoDB
    path('users/<int:id>/stats/', get_user_stats, name='get_user_stats'),
    path('treasures/user/<str:id>/', get_user_treasures, name='get_user_treasures'),
]
