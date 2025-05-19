from django.shortcuts import redirect
from django.urls import reverse

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # URLs que requieren autenticación
        protected_routes = [
            '/models/contenidos/select-categorias/',
            ]
        
        # Comprueba si la URL actual está en las rutas protegidas
        if any(request.path.startswith(url) for url in protected_routes):
            if not request.user.is_authenticated:
                return redirect(reverse('login'))
                
        response = self.get_response(request)
        return response