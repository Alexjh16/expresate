function selectVideo(idVideo) {
    const xhr = new XMLHttpRequest();
    const url = "/models/expresate/clase/seletc/idVideo/";
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrfToken);

    //const data = `idVideo=${encodeURIComponent(idVideo)}`;

    const dato = {
        idVideo: idVideo
    }
    xhr.send(JSON.stringify(dato));

    xhr.onload = function() {
        if (xhr.status === 200) {
            respuesta = JSON.parse(xhr.responseText)
            let id = respuesta.id
            let video = respuesta.videoUrl          
            console.log(respuesta);
            //Colocar la URL del video en el atributo 'src' del <source> y recargar el video
            let etiquetavideo = document.getElementById("videoSelect");
            etiquetavideo.src = video;
            //Se valida si el video fue visto completamente para hacer el cambio de estado en db.    
            let videoTag = document.getElementById("ventanaVideo");
            videoTag.addEventListener('ended', () =>{
                estadoVideo(id);
            })
            videoTag.load();
        } else {
            console.error("Error en la solicitud:", xhr.status, xhr.statusText);
        }
    };
}
//Funcion para hacer el cambio de estado de la db si el video se vio completo
function estadoVideo(id) {
    const xhr = new XMLHttpRequest();
    const url = "/models/expresate/clase/seletc/idVideo/";
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrfToken);

    const dato = {
        estadoVideo: true,
        id: id
    }
    xhr.send(JSON.stringify(dato));

    xhr.onload = function() {
        if (xhr.status === 200) {
            respuesta = JSON.parse(xhr.responseText)
            console.log(respuesta)
        } else {
            console.error("Error en la solicitud:", xhr.status, xhr.statusText);
        }
    };
    console.log("video completo");
}