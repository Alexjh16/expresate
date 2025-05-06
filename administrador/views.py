from django.shortcuts import render

from contenidos.models import CategoriaClases

def index(request):
    return render(request, 'view_admin/app_admin/base_admin.html', {})

def createCategoriaClases(request):
    print('createCategoriaClases', request)
    if request.method == 'POST':
        categoriaClase = CategoriaClases.objects.create(
            nombre_categoria = request.POST['nombre'],
            descripcion = request.POST['descripcion'],
            edad_minima = request.POST['edad_minima'],
            icono = request.POST['icono']
        )
        return render(request, 'view_admin/agregar_categoriaClase.html', {})