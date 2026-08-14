let detenido = false; // Bandera global para controlar si se detuvo
let hablando = false; // Bandera para controlar si se está hablando
let hablandoCampo = false; // Nueva bandera para controlar si se está hablando un campo específico

function hablarInformacion() {
    if (hablando) { // Verifica si ya se está hablando
        // Mostrar alerta si ya está en ejecución
        Swal.fire({
            icon: 'info',
            title: 'Voz ya está en ejecución',
            text: 'Por favor, espere a que termine o presione Detener.'
        });
        return; // Salir de la función si ya está en ejecución
    }

    detenido = false; // Reiniciar la bandera al iniciar la función
    hablando = true; // Marcar que se está hablando

    // Desactivar botones de hablar de campos
    desactivarBotonesHablar();

    const duiExp = document.getElementById('duiExp').value.trim();
    const nombreMascota = document.getElementById('nombreMascota').value.trim();
    const sexo = document.getElementById('sexo').value.trim();
    const especie = document.getElementById('especie').value.trim();
    const raza = document.getElementById('raza').value.trim();
    const edad = document.getElementById('edad').value.trim();
    const detalles = document.getElementById('detalles').value.trim();
    const peso = document.getElementById('peso').value.trim();

    const checkboxesE = document.querySelectorAll('input[id="enfermedades"]:checked');
    const enfermedades = Array.from(checkboxesE).map(checkbox => checkbox.value).join(', ');

    const esterilizado = document.getElementById('esterilizado').value.trim();

    const checkboxesV = document.querySelectorAll('input[id="vacunas"]:checked');
    const vacunas = Array.from(checkboxesV).map(checkbox => checkbox.value).join(', ');

    const checkboxesX = document.querySelectorAll('input[id="examenes"]:checked');
    const examenes = Array.from(checkboxesX).map(checkbox => checkbox.value).join(', ');
    //const examenes = document.getElementById('examenes').value.trim();
    const observacionexamenes = document.getElementById('observacionexamenes').value.trim();
    const desparacitaciones = document.getElementById('desparacitaciones').value.trim();
    const ultcita = document.getElementById('ultcita').value.trim();
    const proxcita = document.getElementById('proxcita').value.trim();
    const descproxcita = document.getElementById('descproxcita').value.trim();
    const descultcita = document.getElementById('descultcita').value.trim();
    const veterinario = document.getElementById('veterinario').value.trim();

    const datos = [];

    if (duiExp) datos.push(`DUI del propietario: ${duiExp}`);
    if (nombreMascota) datos.push(`Nombre de la mascota: ${nombreMascota}`);
    if (sexo) datos.push(`Sexo de la mascota: ${sexo}`);
    if (especie) datos.push(`Especie de la mascota: ${especie}`);
    if (raza) datos.push(`Tipo de raza: ${raza}`);
    if (edad) datos.push(`Edad: ${edad}`);
    if (detalles) datos.push(`Detalles de la mascota: ${detalles}`);
    if (peso) datos.push(`Peso de la mascota: ${peso}`);
    if (enfermedades) datos.push(`Enfermedades: ${enfermedades}`);
    if (esterilizado) datos.push(`Esterilizado: ${esterilizado}`);
    if (vacunas) datos.push(`Vacunas: ${vacunas}`);
    if (examenes) datos.push(`Exámenes: ${examenes}`);
    if (observacionexamenes) datos.push(`Observaciones de historial: ${observacionexamenes}`);
    if (desparacitaciones) datos.push(`Desparacitaciones: ${desparacitaciones}`);
    if (ultcita) datos.push(`Última cita: ${ultcita}`);
    if (descultcita) datos.push(`Descripción de Última cita: ${descultcita}`);
    if (proxcita) datos.push(`Próxima cita: ${proxcita}`);
    if (descproxcita) datos.push(`Descripción de Próxima cita: ${descproxcita}`);
    if (veterinario) datos.push(`Veterinario encargado: ${veterinario}`);

    if (datos.length === 0) {
        datos.push('No hay ningún campo llenado.');
    }

    // Introducción antes de comenzar a hablar
    const introduccion = "La información del expediente es la siguiente.";
    
    const textoCompleto = [introduccion, ...datos].join('. ');

    // Dividir en fragmentos pequeños (máximo 150 caracteres por fragmento)
    const fragmentos = textoCompleto.match(/.{1,100}(\.|$)/g);

    let index = 0; // Índice actual del fragmento

    function hablarSiguienteFragmento() {
        if (detenido || index >= fragmentos.length) {
            hablando = false; // Marcar que ya no se está hablando
            reactivarBotonesHablar(); // Reactivar botones al finalizar
            return; // Detener si se marcó 'detenido' o no hay más fragmentos
        }

        const utterance = new SpeechSynthesisUtterance(fragmentos[index]);
        utterance.lang = 'es-US';

        utterance.onend = function () {
            if (!detenido) {
                setTimeout(() => {
                    index++;
                    hablarSiguienteFragmento();
                }, 100); // Retraso entre fragmentos
            }
        };

        utterance.onerror = function (e) {
            //console.error("Error al hablar el fragmento: ", e.error);
            index++;
            hablarSiguienteFragmento(); // Continuar con el siguiente fragmento
        };

        speechSynthesis.speak(utterance);
    }

    hablarSiguienteFragmento(); // Iniciar hablando
}

function detenerHablar() {
    detenido = true; // Marcar que se detenga todo
    speechSynthesis.cancel(); // Detener la síntesis de voz
}

function hablarCampo(campoId, nombreCampo) {
    if (hablando) { // Verifica si ya se está hablando el expediente completo
        Swal.fire({
            icon: 'info',
            title: 'No se puede hablar este campo',
            text: 'Por favor, espere a que termine de hablar el expediente completo.'
        });
        return; // Salir si ya se está hablando el expediente completo
    }

   hablandoCampo = true; // Marcar que se está hablando un campo específico

   const valorCampo = document.getElementById(campoId).value.trim();
    
   let texto;
   
   if (valorCampo) {
       texto = `${nombreCampo}: ${valorCampo}`;
   } else {
       texto = `No hay información para este campo.`;
   }

   const utterance = new SpeechSynthesisUtterance(texto);
   
   utterance.lang = 'es-US';

   speechSynthesis.cancel(); // Cancelar cualquier síntesis en curso
   speechSynthesis.speak(utterance);

   utterance.onend = function () {
       hablandoCampo = false; // Marcar que ya no se está hablando este campo
   };
}

function hablarCampoCheck(campoId, nombreCampo) {
    if (hablando) { // Verifica si ya se está hablando el expediente completo
        Swal.fire({
            icon: 'info',
            title: 'No se puede hablar este campo',
            text: 'Por favor, espere a que termine de hablar el expediente completo.'
        });
        return; // Salir si ya se está hablando el expediente completo
    }

   hablandoCampo = true; // Marcar que se está hablando un campo específico

   const checkboxes = document.querySelectorAll(`input[id="${campoId}"]:checked`);
   const seleccionados = Array.from(checkboxes).map(checkbox => checkbox.value).join(', ');

   let texto;

   if (seleccionados) {
       texto = `${nombreCampo}: ${seleccionados}`;
   } else {
       texto = `No hay información para este campo.`;
   }

    const utterance = new SpeechSynthesisUtterance(texto);
   
   utterance.lang = 'es-US';

   speechSynthesis.cancel(); // Cancelar cualquier síntesis en curso
   speechSynthesis.speak(utterance);

   utterance.onend = function () {
       hablandoCampo = false; // Marcar que ya no se está hablando este campo
   };
}

// Función para desactivar los botones de hablar en los campos
function desactivarBotonesHablar() {
   const botonesHablar = document.querySelectorAll('.custom-button');
   botonesHablar.forEach(boton => {
       boton.disabled = true; // Desactiva cada botón
   });
}

// Función para reactivar los botones de hablar en los campos
function reactivarBotonesHablar() {
   const botonesHablar = document.querySelectorAll('.custom-button');
   botonesHablar.forEach(boton => {
       boton.disabled = false; // Reactiva cada botón
   });
}
