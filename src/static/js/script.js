function reconocerVoz(campo) {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'es-ES';

    recognition.onstart = function() {
        console.log("Reconocimiento de voz iniciado.");
    };

    recognition.onresult = function(event) {
        let transcript = event.results[0][0].transcript;

        // Convertir la primera letra a mayúscula
        transcript = transcript.charAt(0).toUpperCase() + transcript.slice(1);

        // Asignar el texto al campo correspondiente
        document.getElementById(campo).value = transcript;

        // Mostrar el resultado en el párrafo correspondiente
        if (campo === 'nombreProp') {
            document.getElementById('resultadoNombreProp').innerText = transcript;
        } else if (campo === 'direccion') {
            document.getElementById('resultadoDireccion').innerText = transcript;
        } else if (campo === 'nombreMascota') {
            document.getElementById('resultadoNombreMascota').innerText = transcript;
        } else if (campo === 'edad') {
            document.getElementById('resultadoEdad').innerText = transcript;
        } else if (campo === 'detalles') {
            document.getElementById('resultadoDetalles').innerText = transcript;
        } else if (campo === 'peso') {
            document.getElementById('resultadoPeso').innerText = transcript;
        } else if (campo === 'enfermedades') {
            document.getElementById('resultadoEnfermedades').innerText = transcript;
        } else if (campo === 'vacunas') {
            document.getElementById('resultadoVacunas').innerText = transcript;
        } else if (campo === 'examenes') {
            document.getElementById('resultadoExamenes').innerText = transcript;
        } else if (campo === 'observacionexamenes') {
            document.getElementById('resultadoExamenesObservacion').innerText = transcript;
        } else if (campo === 'desparacitaciones') {
            document.getElementById('resultadoDesparacitaciones').innerText = transcript;
        } else if (campo === 'ultcita') {
            document.getElementById('resultadoUltCita').innerText = transcript;
        } else if (campo === 'proxcita') {
            document.getElementById('resultadoProxCita').innerText = transcript;
        } else if (campo === 'descultcita') {
            document.getElementById('resultadoDescUltCita').innerText = transcript;
        } else if (campo === 'descproxcita') {
            document.getElementById('resultadoDescProxCita').innerText = transcript;
        }
    };

    recognition.onerror = function(event) {
        console.error("Error de reconocimiento: ", event.error);
    };

    recognition.start();
}

function reconocerVozSexo(campo) {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'es-ES';

    recognition.onstart = function() {
        console.log("Reconocimiento de voz iniciado.");
    };

    recognition.onresult = function(event) {
        let transcript = event.results[0][0].transcript;

        // Capitalizar la primera letra
        transcript = transcript.charAt(0).toUpperCase() + transcript.slice(1).toLowerCase();

        // Palabras relacionadas con "Macho" y "Hembra"
        const machoWords = ["Macho", "Hombre", "Varón", "Masculino", "Niño", "Chico"];
        const hembraWords = ["Hembra", "Mujer", "Femenino", "Niña", "Chica", "Princesa"];

        // Limpiar el campo antes de asignar un valor
        document.getElementById(campo).value = "";

        // Evaluar el resultado y asignar valores
        if (machoWords.includes(transcript)) {
            document.getElementById('resultadoSexo').innerText = "Macho";
            document.getElementById(campo).value = "Macho";
        } else if (hembraWords.includes(transcript)) {
            document.getElementById('resultadoSexo').innerText = "Hembra";
            document.getElementById(campo).value = "Hembra";
        } else {
            document.getElementById('resultadoSexo').innerText = "Ingrese un sexo válido";
        }
    };

    recognition.onerror = function(event) {
        console.error("Error de reconocimiento: ", event.error);
    };

    recognition.start();
}

function reconocerVozEspecie(campo) {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'es-ES';

    recognition.onstart = function () {
        console.log("Reconocimiento de voz iniciado.");
    };

    recognition.onresult = function (event) {
        let transcript = event.results[0][0].transcript;

        // Capitalizar la primera letra y hacer el resto minúscula
        transcript = transcript.charAt(0).toUpperCase() + transcript.slice(1).toLowerCase();

        // Palabras relacionadas con "Canino" y "Felino"
        const caninoWords = [
            "Canino", "Perro", "Perra", "Perrito", "Perrita", 
            "Chucho", "Chucha", "Chuchito", "Chuchita"
        ];
        const felinoWords = [
            "Felino", "Gato", "Gata", "Gatito", "Gatita", 
            "Mish", "Minino", "Minina"
        ];

        // Limpiar el campo antes de asignar un valor
        document.getElementById(campo).value = "";

        // Evaluar el resultado y asignar valores
        if (caninoWords.includes(transcript)) {
            document.getElementById('resultadoEspecie').innerText = "Canino";
            document.getElementById(campo).value = "Canino";
        } else if (felinoWords.includes(transcript)) {
            document.getElementById('resultadoEspecie').innerText = "Felino";
            document.getElementById(campo).value = "Felino";
        } else {
            document.getElementById('resultadoEspecie').innerText = "Debes ingresar una especie válida";
        }

        // Llamar a la función updateRaza si corresponde
        updateRaza();
    };

    recognition.onerror = function (event) {
        console.error("Error de reconocimiento: ", event.error);
    };

    recognition.start();
}



function updateRaza() {
    const especieSelect = document.getElementById('especie');
    const razaSelect = document.getElementById('raza');
    const selectedEspecie = especieSelect.value;

    // Limpiar opciones anteriores
    razaSelect.innerHTML = '';

    let razas = [];
    if (selectedEspecie === 'Canino') {
        razas = ['Mestizo','Bulldog', 'Chihuahua', 'Dachshund', 'Golden Retriever', 'Labrador Retriever', 'Poodle', 'Rottweiler', 'Boxer', 'Yorkshire Terrier', 'Pastor Alemán', 'Pug', 'Shih Tzu'];
    } else if (selectedEspecie === 'Felino') {
        razas = ['Mestizo','Angora','American Shorthair', 'Bengala', 'British Shorthair', 'Maine Coon', 'Persa', 'Ragdoll', 'Russian Blue', 'Scottish Fold', 'Siamés', 'Sphynx', 'American Shorthair', 'British Shorthair'];
    }

    // Agregar nuevas opciones
    razas.forEach(raza => {
        const option = document.createElement('option');
        option.value = raza.toLowerCase();
        option.textContent = raza;
        razaSelect.appendChild(option);
    });
}

