from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login #aca se se coloca un alias al metodo login se manda a llamar esto se hace porqeu hay una funcion llamada login y causa conflitos. lo mismo se hace con logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import *
import json

# Creacion de usuario

#Iniciar o autenticar un usuario  
#Cerrar Session     
# Se Crea la categoria o el modulo de la clase
def createCategoriaClases(request):
    if request.method == 'POST':
        categoriaClase = CategoriaClases.objects.create(
            nombre_categoria = request.POST['nombre'],
        )
        return render(request, 'view_admin/agregar_categoriaClase.html', {})
    
    
#creacion de videos y categorias de clases   
def indexCreateVideo(request):
    arrayCategoriaClases = CategoriaClases.objects.all().order_by('nombre_categoria')
    return render(request, 'view_admin/agregar_video.html', {'arrayCategoriaClases': arrayCategoriaClases})

#Se guarda el video y las imagenes o las url en ma base de datos
def createVideoClases(request):
    if request.method == 'POST':
        #Se captura el id de la categoria de clases desde formulario para llamar una istancia
        idCategoriaClase = request.POST.get('categoriaClase')
        categoria = CategoriaClases.objects.get(id=idCategoriaClase)
        #Se agrega el video y la imagen al la DB de datos
        createVideoClase = Videos.objects.create(
            imagen = request.FILES.get('imagen'),
            video = request.FILES.get('video'),
            nombre_sena = request.POST['nombre'],
        )
        #Se le agrega el video a la categria de clase que pertenece
        videosCategoriaClase = VideosCategoriaClase.objects.create(
            categoriaClases = categoria,
            videos = createVideoClase,
        )      
        return HttpResponse(f'Video y categoría creados exitosamente. ID: {videosCategoriaClase.id}')
        #return render(request, 'view_admin/agregar_video.html', {message: messages})

#Metodo para selecionar i enviar todas las categoria o modulos al formulario de creacion de video  
def moduloClase(request, NM):    
    # Filtra las categorías por el nombre de la categoría
    print(NM)
    categorias = CategoriaClases.objects.all()
    cursos = Cursos.objects.filter(categoria_clase__nombre_categoria=NM)
    nombre_categoria = categorias[0].nombre_categoria if categorias.exists() else None
    return render(request, 'modulo_clase.html', {'categorias':categorias, 'cursos':cursos, 'nombre_categoria': nombre_categoria})


def seletcVideo(request):
    if request.method == 'POST':
        #Se cambia de estado si vio el video completo
        datosEstadoVideo = json.loads(request.body)
        if datosEstadoVideo.get('estadoVideo') == True:
            Usuarios_videos_categoria.objects.filter(videos = datosEstadoVideo.get('id')).update(estadoVideo = True)
            return JsonResponse({'mensaje':'estado Actualizado con exito'})
        else:
            #se captura el id del usuario esta en seccion 
            usuario = request.user         
            idVideo = json.loads(request.body)      #Se recupera el id del video que se quiere ver 
            intIdVideo = int(idVideo.get('idVideo'))    #Se convierte a entero porque se resive un string
            print(intIdVideo)
            idVideoMenosUno = intIdVideo - 1    #Se le resta 1 al id para buscar el vidoe anterior y chequear si su estado es true o falso
            print(idVideoMenosUno)      
            if intIdVideo <=1:
                seletcVideo = Videos.objects.get(id = intIdVideo)
                print(seletcVideo.video.url)
                #Se almacenan los videos y datos del usuario que el usuario se ha visto para realizar las validaciones de los videos que se an visto 
                Usuarios_videos_categoria.objects.create(
                     usuario = usuario,
                     videos = seletcVideo,
                    )
                #Se crea un dicionario con los datos del video. se convierte a formato JSON y se envia via ajax request
                videoDato = {
                     'id': seletcVideo.id,
                     'nombre_sena': seletcVideo.nombre_sena,
                     'videoUrl': seletcVideo.video.url,  
                     'imagenUrl': seletcVideo.imagen.url,                
                    }
                return JsonResponse(videoDato)
            elif intIdVideo >= 1:                      
                arrayVideos = Usuarios_videos_categoria.objects.filter(usuario = request.user.id)  #Se hacer una query a la tabla pivote para traer todos los videos vistos que coresponden a ese id de usuario
                print('entra')
                for item in arrayVideos:
                    print(item.videos.id)
                    if idVideoMenosUno == item.videos.id:   #Se valida si el id menos uno existe en la table, si existe deja pasar para validar su estado  
                        if item.estadoVideo: #Se valida el estado del video si es true envia el video de la peticion
                            #Se selecciona el video de la peticion con el id especifico
                            seletcVideo = Videos.objects.get(id = idVideo.get('idVideo'))
                            categoriaclase = VideosCategoriaClase.objects.get(videos__id=seletcVideo.id)
                            #Se almacenan los videos y datos del usuario que el usuario se ha visto para realizar las validaciones de los videos que se an visto 
                            Usuarios_videos_categoria.objects.create(
                                usuario = usuario,
                                videos = seletcVideo,
                            )
                            #Se crea un dicionario con los datos del video. se convierte a formato JSON y se envia via ajax request
                            videoDato = {
                                'id': seletcVideo.id,
                                'nombre_sena': seletcVideo.nombre_sena,
                                'videoUrl': seletcVideo.video.url,  
                                'imagenUrl': seletcVideo.imagen.url,                
                            }
                            return JsonResponse(videoDato)
            return JsonResponse({'mensaje':'Deves verte el vidio anterior'})