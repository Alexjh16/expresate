function validarRespuestas() {

    const formulario = document.getElementById('formularioEvaluacion');
    const nombreCategoria = document.getElementById('nombreCategoria').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const formData = new FormData(formulario);
    const respuestasUsuario = Object.fromEntries(formData);

    // Sacar el valor de cada punto para obtener la nota final del modulo
    let l = longitudFormulario = Object.keys(respuestasUsuario).length/2;
    let valorNotaRespuesta = 5/l;
    console.log('Valor nota por cada punto: ' + valorNotaRespuesta);

    let preguntasBuenas = [];
    let preguntasMalas = [];

    Object.keys(respuestasUsuario).forEach(key => {
        if (key.startsWith("p_")) {
            const preguntaId = key.split("_")[1]; //key.split("_") divide el valor de key en un array usando "_" como delimitador. Por ejemplo, "p_1".split("_") devuelve ["p", "1"]. [1] toma el segundo elemento del array, que es el número de la pregunta ("1" en este caso). Así, preguntaId guarda el número de la pregunta actual como una cadena ("1", "2", etc.).
            const respuestaUsuario = respuestasUsuario[key];
            const respuestaCorrecta = respuestasUsuario[`rc_${preguntaId}`];
            const esCorrecto = respuestaUsuario === respuestaCorrecta;
            if(esCorrecto){
                preguntasBuenas.push(1)
            }else{
                preguntasMalas.push(1)
            }
            //console.log(`Pregunta ${preguntaId}: Seleccionada: ${respuestaUsuario}, Correcta: ${respuestaCorrecta}, Resultado: ${esCorrecto ? 'Correcta' : 'Incorrecta'}`);
        }
    });
    
    let notaFinalModulo = preguntasBuenas.length * valorNotaRespuesta

    const xhr = new XMLHttpRequest();
    const url = "/models/evaluacion/estudiante/nota/";

    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-CSRFToken', csrfToken);

    const dato = {
        nombreCategoria:nombreCategoria,
        preguntasBuenas:preguntasBuenas.length,
        preguntasMalas:preguntasMalas.length,
        notaFinalModulo:notaFinalModulo
    }
    xhr.send(JSON.stringify(dato));

    xhr.onload = function() {
        if (xhr.status === 200) {
            respuesta = JSON.parse(xhr.responseText);
            let mensaje = respuesta.success;
            mensajes(mensaje);
        };
    };
    console.log('Nombre categaria: ' + nombreCategoria);
    console.log('Preguntas corretas: ' + preguntasBuenas.length);
    console.log('Preguntas incorretas: ' + preguntasMalas.length);
    console.log('Notal final Modulo=> ' + notaFinalModulo); 
}
function mensajes(mensaje){
    let contenedor = document.createElement('div');
    contenedor.className = `mensaje`;
    contenedor.textContent = mensaje;
    document.body.appendChild(contenedor);

    setTimeout(() => {
        contenedor.remove();
    }, 5000);
}