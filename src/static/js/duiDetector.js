const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture');
const clearButton = document.getElementById('clear');
const toggleCameraButton = document.getElementById('toggleCamera');
const duiInput = document.getElementById('duiExp');
const notification = document.getElementById('notification');

let stream; // Variable para almacenar la transmisión de la cámara
let cameraOn = false; // Estado de la cámara

// Función para encender/apagar la cámara
toggleCameraButton.addEventListener('click', () => {
    if (cameraOn) {
        // Apagar cámara
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        video.srcObject = null; // Detener la transmisión
        toggleCameraButton.textContent = "Encender cámara"; // Cambiar texto del botón
        toggleCameraButton.style.backgroundColor = "#f8f1e7"; // Cambiar a verde
        toggleCameraButton.style.color = "#ee6543"; // Cambiar a rojo
        cameraOn = false; // Actualizar estado
    } else {
        // Encender cámara
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(s => {
                stream = s;
                video.srcObject = stream;
                toggleCameraButton.textContent = "Apagar cámara"; // Cambiar texto del botón
                toggleCameraButton.style.backgroundColor = "#ff6f61"; // Cambiar a rojo
                toggleCameraButton.style.color = "#f8f1e7"; // Cambiar a rojo
                cameraOn = true; // Actualizar estado
            })
            .catch(err => {
                showNotification(`Error al acceder a la cámara: ${err.message}`);
            });
    }
});

// Capturar imagen y realizar OCR
captureButton.addEventListener('click', () => {
    if (!cameraOn) {
        showNotification("Primero enciende la cámara.");
        return;
    }
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);

    preprocessImage(canvas); // Preprocesar imagen

    Tesseract.recognize(
        canvas,
        'spa',
        {
            logger: info => console.log(info)
        }
    ).then(({ data: { text } }) => {
        console.log("Texto extraído:", text);
        const duiMatch = text.match(/\b\d{8}-\d\b/);
        if (duiMatch) {
            duiInput.value = duiMatch[0]; // Mostrar el DUI escaneado
            console.log("DUI extraído:", duiMatch[0]); // Imprimir en la consola
        } else {
            showNotification("No se pudo encontrar el número de DUI.");
        }
    }).catch(err => {
        showNotification(`Error en Tesseract: ${err.message}`);
    });
});

// Función para limpiar el campo de DUI
clearButton.addEventListener('click', () => {
    duiInput.value = ''; // Limpiar el campo de entrada
    // Se eliminó el mensaje de campo limpiado
});

function preprocessImage(canvas) {
    const context = canvas.getContext('2d');
    const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    for (let i = 0; i < data.length; i += 4) {
        const avg = (data[i] + data[i + 1] + data[i + 2]) / 3; 
        data[i] = avg;     // Rojo
        data[i + 1] = avg; // Verde
        data[i + 2] = avg; // Azul
    }
    context.putImageData(imageData, 0, 0);
}

function showNotification(message) {
    notification.textContent = message;
    notification.style.display = "block";
    notification.style.background = "#ff6f61"; // Error
    setTimeout(() => {
        notification.style.display = "none";
    }, 3000);
}