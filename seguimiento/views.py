from datetime import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from mongoData.models import Treasures
from math import radians, cos, sin, asin, sqrt
import json

# Create your views here.
#GET /api/treasures/nearby/ - Tesoros cercanos
def get_nearby_treasures(request):
    #send a valid lat, lng and radius in km as query params
    #example: /api/treasures/nearby/?lat=40.7128&lng=-74.0060&radius=5
    try:
        lat = float(request.GET.get('lat'))
        lng = float(request.GET.get('lng'))
        radius = float(request.GET.get('radius', 5))  # radio en km
    except (TypeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Parámetros inválidos'}, status=400)

    #listar tesoros cercanos (lógica simulada) desde mongoDB
    if request.method != 'GET':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
    try:
         # Convertir radio de km a metros
        radius_m = radius * 1000
        # Consulta geoespacial usando mongoengine
        # location__near busca puntos cerca de [lng, lat], max_distance en metros
        qs = Treasures.objects(location__near=[lng, lat], location__max_distance=radius_m)

        results = []

        for t in qs:
            # Calcular distancia usando Haversine
            dist = haversine_distance(lat, lng, float(t.latitude), float(t.longitude))

            results.append({
                'id': str(t.id),
                'creator_id': t.creator_id,
                'creator_name': t.creator_name,
                'title': t.title,
                'description': t.description,
                'image_url': t.image_url,
                'latitude': t.latitude,
                'longitude': t.longitude,
                'hint': t.hint,
                'difficulty': t.difficulty,
                'clues': t.clues,
                'is_found': t.is_found,
                'found_by': t.found_by,
                'created_at': t.created_at.isoformat() if t.created_at else None,
                'found_at': t.found_at.isoformat() if t.found_at else None,
                'points': t.points,
                'distance_km': round(dist, 2)
            })
        return JsonResponse({'success': True, 'treasures': results}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia en km entre dos puntos usando la fórmula de Haversine
    """
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radio de la Tierra en km
    return c * r

#POST /api/treasures/ - Crear tesoro
@csrf_exempt
def create_treasure(request):
    if request.method == 'POST':

        #data example body
        """
        {
            "creator_id": "609c5d2f8f1b2c0015b8e4d2",
            "creator_name": "Juan Perez",
            "title": "Tesoro Escondido",
            "description": "Encuentra el tesoro escondido en el parque.",
            "location": {"type": "Point", "coordinates": [-74.0060, 40.7128]},
            "image_url": "http://example.com/image.png",
            "latitude": "40.7128",
            "longitude": "-74.0060",
            "hint": "Cerca del árbol grande.",
            "difficulty": 3,
            "clues": ["Busca cerca del banco", "Mira debajo de las hojas"],
            "points": 50
        }
        """
        try:
            data = json.loads(request.body)
            new_treasure = Treasures(
                creator_id=data.get('creator_id'),
                creator_name=data.get('creator_name'),
                title=data.get('title'),
                description=data.get('description'),
                location=data.get('location'),
                image_url=data.get('image_url'),
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                hint=data.get('hint'),
                difficulty=data.get('difficulty', 1),
                clues=data.get('clues', []),
                is_found=False,
                found_by=None,
                points=data.get('points', 0)
            )
            new_treasure.save()
        except  Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'success': True, 'message': 'Tesoros creado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

#POST /api/treasures/{id}/claim/ - Reclamar tesoro
@csrf_exempt
def claim_treasure(request, id):
    #id = objectId of treasure, and claim treasure and set is_found to True, found_by (ObcjectId of user) and found_at (current datetime)

    #url example: /api/treasures/68fb9b7aeb90222b049ee71b/claim/
    #body example
    """
    {
        "user_id": "68fb6a4d87f47d9e4d229b23"
    }
    """
    #68fb9b7aeb90222b049ee71b
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            treasure = Treasures.objects.get(id=id)
            if treasure.is_found:
                return JsonResponse({'success': False, 'error': 'Tesoro ya reclamado'}, status=400)
            # Obtener user_id del JSON
            user_id = data.get('user_id')
            if not user_id:
                return JsonResponse({'success': False, 'error': 'user_id requerido'}, status=400)
            treasure.is_found = True
            treasure.found_by = user_id
            treasure.found_at = datetime.utcnow()
            treasure.save()
        except Treasures.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tesoro no encontrado'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
        return JsonResponse({'success': True,'message': f'Tesoro {id} reclamado'})
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
#GET /api/treasures/user/{id}/ - Tesoros del usuario
@csrf_exempt
def get_user_treasures(request, id):
    #id = objectId of user

    #uri example: /api/treasures/user/68fb6a4d87f47d9e4d229b23/
    #body example
    """
    {
        "user_id": "68fb6a4d87f47d9e4d229b23"
    }
    """
    try:
        user_treasures = Treasures.objects(found_by=id)
        user_treasures = [{
            'id': str(t.id),
            'creator_id': t.creator_id,
            'creator_name': t.creator_name,
            'title': t.title,
            'description': t.description,
            'image_url': t.image_url,
            'latitude': t.latitude,
            'longitude': t.longitude,
            'hint': t.hint,
            'difficulty': t.difficulty,
            'clues': t.clues,
            'is_found': t.is_found,
            'found_by': t.found_by,
            'created_at': t.created_at.isoformat() if t.created_at else None,
            'found_at': t.found_at.isoformat() if t.found_at else None,
            'points': t.points
        } for t in user_treasures]
        return JsonResponse({'success': True, 'user_treasures': user_treasures})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

#GET /api/users/{id}/stats/ - Estadísticas
@csrf_exempt
def get_user_stats(request, id):
    return JsonResponse({'message': f'Estadísticas del usuario {id}'})
