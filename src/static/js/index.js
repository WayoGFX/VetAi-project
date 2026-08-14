const video = document.createElement("video");

// Canvas para mostrar la cámara
const canvasElement = document.getElementById("qr-canvas");
const canvas = canvasElement.getContext("2d", { willReadFrequently: true });

// Elementos de la interfaz
const btnScanQR = document.getElementById("btn-scan-qr");
const vetKeyInput = document.getElementById("VetKey");
const submitBtn = document.getElementById("submit-btn");

// Variables de control
let scanning = false;
let cameraActive = false;
let scannedValue = ""; // Almacenar la respuesta del QR
let qrSent = false; // Controlar si el QR ya ha sido enviado

// Función para encender la cámara
const encenderCamara = () => {
  if (cameraActive) {
    Swal.fire("Advertencia", "La cámara ya está activa.", "warning");
    return;
  }

  navigator.mediaDevices
    .getUserMedia({ video: { facingMode: "environment" } })
    .then(function (stream) {
      scanning = true;
      cameraActive = true;
      btnScanQR.hidden = true;
      canvasElement.hidden = false;
      video.setAttribute("playsinline", true); // Requerido para iOS Safari
      video.srcObject = stream;
      video.play();
      tick();
      scan();
    })
    .catch(function (error) {
      Swal.fire("Error", "No se pudo acceder a la cámara: " + error.message, "error");
    });
};

// Función para actualizar el canvas con la imagen del video
function configurarCanvas() {
  canvasElement.height = video.videoHeight;
  canvasElement.width = video.videoWidth;
}

function tick() {
  configurarCanvas();
  canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);
  if (scanning) {
    requestAnimationFrame(tick);
  }
}

// Escanear el código QR
function scan() {
  try {
    qrcode.decode();
  } catch (e) {
    setTimeout(scan, 300);
  }
}

// Apagar la cámara
const cerrarCamara = () => {
  if (!cameraActive) {
    Swal.fire("Error", "No hay cámaras activas.", "error");
    return;
  }

  video.srcObject.getTracks().forEach((track) => track.stop());
  cameraActive = false;
  scanning = false;
  canvasElement.hidden = true;
  btnScanQR.hidden = false;
};

// Activar sonido al leer el código QR
const activarSonido = () => {
  const audio = document.getElementById("audioScaner");
  audio.play();
};

// Callback para manejar la lectura del código QR -- MODIFICADO POR WAYO
qrcode.callback = (respuesta) => {
  if (respuesta) {
      // Muestra el mensaje de éxito
      Swal.fire({
          title: "Código Escaneado",
          text: `Código: ${respuesta}`,
          icon: "success",
          confirmButtonText: "OK"
      }).then((result) => {
          if (result.isConfirmed) {
              // Asignar el valor escaneado al input oculto
              vetKeyInput.value = respuesta;

              // Enviar el formulario
              document.getElementById("qr-form").submit();
          }
      });

      // Almacenar la respuesta en una variable global
      scannedValue = respuesta;

      activarSonido();
      cerrarCamara();
  }
};

// Manejar el botón de enviar
submitBtn.addEventListener("click", () => {
  if (!scannedValue) {
    Swal.fire("Error", "No se ha escaneado ningún código QR.", "error");
    return;
  }

  if (qrSent) {
    Swal.fire("Información", "Solo puedes enviar el código QR una vez. Refresca la página para volver a escanear.", "info");
    return;
  }

  // Asignar el valor escaneado al input oculto
  vetKeyInput.value = scannedValue;

  // Mostrar en consola para verificar
  console.log("VetKey:", vetKeyInput.value);

  // Marcar que el QR ha sido enviado
  qrSent = true;

  // Notificar al usuario que se envió exitosamente
  Swal.fire("Éxito", "Código QR enviado exitosamente.", "success");

  // Enviar el formulario (opcional)
  // form.submit();
});
