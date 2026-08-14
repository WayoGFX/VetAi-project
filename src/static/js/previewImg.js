document.getElementById('imageMascota').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const preview = document.getElementById('previewImage');

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result; // Muestra la imagen cargada
        }
        reader.readAsDataURL(file); // Lee la imagen como URL de datos
    } else {
        preview.src = '/path/to/default-image.jpg'; // Reemplaza con la ruta de la imagen por defecto
    }
});