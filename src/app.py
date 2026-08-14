from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import qrcode
from PIL import Image, ImageDraw, ImageFont
import base64
import os
import io
from io import BytesIO
#PARA EL CHATBOT
import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
import difflib  # Importar la biblioteca para coincidencias de similitud

load_dotenv()
api_key = os.getenv('API_KEY')

#CONFIG
if not api_key:
    raise ValueError("No se encontró la API_KEY en el archivo .env")

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

def generar_respuesta_veterinaria(nombre_animal, especie, edad, sexo, sintomas, antecedentes):
    contents = {
        'text': (
            f"Eres un asistente veterinario profesional. Proporciona una respuesta clara y compacta, hazlo en 2 párrafos. tienes que terminar con esto: Para más información visita nuestra veterinaria en la Universidad Salvadoreña Alberto Masferrer, gracias, "
            f"Realizar la respuesta basado en los siguientes datos del paciente:\n\n"
            f"- **Nombre:** {nombre_animal}\n"
            f"- **Especie:** {especie}\n"
            f"- **Edad:** {edad}\n"
            f"- **Sexo:** {sexo}\n"
            f"- **Síntomas:** {sintomas}\n"
            f"- **Antecedentes:** {antecedentes}\n\n"
            "### Consejos prácticos para el dueño:\n"
            "- Asegúrate de mantener al animal hidratado.\n"
            "- Observa cualquier cambio en su comportamiento.\n"
            "- Consulta a un veterinario si los síntomas persisten."
        )
    }
    response = model.generate_content(contents=contents)
    return response.text.replace(". ", ".\n\n")

app = Flask(__name__)

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'vet_ai'

mysql = MySQL(app)

# Enrutamiento inicio de sesión
@app.route('/')
def index():
    return render_template('index.html')

# Enrutamiento inicio
@app.route('/propSesion', methods=['GET', 'POST'])
def propSesion():
    return render_template('propietarioSesion.html')

# Enrutamiento Añadir nuevo propietario
@app.route('/addProp', methods=['GET', 'POST'])
def addProp():
    return render_template('addPropietario.html')

# Proceso para almacenar datos de Propietarios
@app.route('/uploadProp', methods=['POST'])
def upload():
    if request.method == 'POST':
        dui = request.form['duiExp']
        nombreProp = request.form['nombreProp']
        imageProp = request.files['imageProp']
        imageProp_data = imageProp.read()
        telefono = request.form['telefono']
        telefono = int(telefono)
        direccion = request.form['direccion']
        correo = request.form['correo']

        # guardar en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Propietario (DUI, NombrePropietario, FotoPropietario, Telefono, Direccion, Correo) VALUES (%s, %s, %s, %s, %s, %s)",(dui, nombreProp, imageProp_data, telefono, direccion, correo))
        mysql.connection.commit()
        cur.close()
        # Redirigir a la página de menu
        return redirect(url_for('addExp'))
    
# Enrutamiento menu principal
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    return render_template('menu.html')

# Enrutamiento Añadir nuevo Expediente
@app.route('/addExp', methods=['GET', 'POST'])
def addExp():
    return render_template('nuevoExpediente.html')


# Proceso para almacenar datos de Expediente
@app.route('/uploadExp', methods=['POST'])
def uploadExp():
    if request.method == 'POST':
        nombreMascota = request.form['nombreMascota']
        sexo = request.form['sexo']
        especie = request.form['especie']
        raza = request.form['raza']
        edad = request.form['edad']
        detalles = request.form['detalles']
        imageMascota = request.files['imageMascota']
        imageMascota_data = imageMascota.read()
        peso = request.form['peso']
        enfermedades = request.form.getlist('enfermedades') # examenes en lista
        enfermedades_str = ', '.join(enfermedades)
        esterilizado = request.form['esterilizado']
        vacunas = request.form.getlist('vacunas') # examenes en lista
        vacunas_str = ', '.join(vacunas)

        examenes = request.form.getlist('examenes') # examenes en lista
        examenes_str = ', '.join(examenes)
        observacionExamenes = request.form['observacionexamenes']
        desparacitaciones = request.form['desparacitaciones']
        ultcita = request.form['ultcita']
        proxcita = request.form['proxcita']
        duiExp = request.form['duiExp']
        image_dataQR = imageMascota_data
        descUltimaCita = request.form['descultcita']
        descProxCita = request.form['descproxcita']
        nombreVeterinario = request.form['veterinario']

        # Verificar si el DUI existe en la tabla Propietario
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM Propietario WHERE DUI = %s", (duiExp,))
        dui_exists = cur.fetchone()[0] > 0
        cur.close()

        if not dui_exists:
            return render_template('404errorDUI.html')  # Redirigir a la página de error si el DUI no existe

        # Guardar en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ExpedienteMascota (NombreMascota, Sexo, Especie, Raza, Edad, Detalles, FotoMascota, Peso, Enfermedades, Esterilizado, Vacunas, Examenes, ObservacionExamenes, Desparasitaciones, UltimaCita, ProxCita, DUI, FotoQR, DescUltimaCita, DescProxCita, NombreVeterinario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)", (nombreMascota, sexo, especie, raza, edad, detalles, imageMascota_data, peso, enfermedades_str, esterilizado, vacunas_str, examenes_str, observacionExamenes, desparacitaciones, ultcita, proxcita, duiExp, image_dataQR, descUltimaCita, descProxCita, nombreVeterinario))
        mysql.connection.commit()
        last_id = cur.lastrowid  # Obtener el último ID insertado
        cur.close()

	#go_p Configuración del QR según especie
    # Configuración del QR según especie
    loath = "static/logo.png"  # Logo predeterminado
    background_color = "#ffffff"  # Color de fondo predeterminado

    if especie.lower() == "felino":
        colorCSS = "stylecorrectG.css" # ESTE ES PARA CAMBIAR EL CSS
        logo_path = "static/gatologo.png"  # Logo para felinos
        background_color = "#70a5ff"  # Fondo para gatos
    elif especie.lower() == "canino":
        colorCSS = "stylecorrectP.css" # ESTE ES PARA CAMBIAR EL CSS
        logo_path = "static/perroLogo.png"  # Logo para Canino
        background_color = "#f5a693"  # Fondo para perros

    # Generar el código QR
    qr = qrcode.QRCode(version=1, box_size=35, border=5)
    qr.add_data(str(last_id))
    qr.make(fit=True)
    img_qr = qr.make_image(fill='black', back_color=background_color)

    # Agregar el logo
    logo = Image.open(logo_path)
    logo = logo.resize((200, 200))  # Ajustar el tamaño del logo
    img_qr = img_qr.convert("RGB")
    img_qr.paste(logo, (img_qr.size[0] // 2 - logo.size[0] // 2, img_qr.size[1] // 2 - logo.size[1] // 2))

    # Añadir el nombre debajo del código QR
    nombre_texto = nombreMascota  # Usar el nombre proporcionado en el formulario
    font_path = "static/fonts/Poppins-Bold.ttf"  # Ruta a la fuente Poppins descargada
    font_size = 160  # Tamaño de la fuente

    # Cargar la fuente
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print("Error al cargar la fuente. Asegúrate de que el archivo de fuente existe.")

    # Crear una nueva imagen para combinar el QR y el texto
    qr_width, qr_height = img_qr.size
    draw_temp = ImageDraw.Draw(img_qr)  # Crea un objeto ImageDraw temporal para calcular dimensiones
    text_bbox = draw_temp.textbbox((0, 0), nombre_texto, font=font)
    text_width = text_bbox[2] - text_bbox[0]  # Ancho del texto
    text_height = text_bbox[3] - text_bbox[1]  # Alto del texto

    img_final = Image.new("RGB", (qr_width, qr_height + text_height + 20), background_color)  # Fondo dinámico

    # Pegar el QR en la imagen final
    img_final.paste(img_qr, (0, 0))

    # Dibujar el texto en la imagen final
    draw = ImageDraw.Draw(img_final)
    text_x = (qr_width - text_width) // 2  # Centrar el texto
    text_y = qr_height - 150  # Posición debajo del QR
    draw.text((text_x, text_y), nombre_texto, font=font, fill="white") # AQUÍ SE CAMBIA EL COLOR

    # Almacenar la imagen final en una variable
    img_byte_arr = BytesIO()
    img_final.save(img_byte_arr, format='PNG')  # Guardar en formato PNG
    img_byte_arr.seek(0)  # Regresar al inicio del objeto BytesIO

    # Ahora puedes usar img_byte_arr para image.read()
    # ESTO ES PARA GUARDAR EL QR EN LA BASE DE DATOS:
    image_dataQR = img_byte_arr.read()  # Leer los datos de la imagen

    # Si necesitas guardar la imagen en disco también, puedes hacerlo
    qr_path = f"static/qr/qrVetAI_{last_id}.png"
    img_final.save(qr_path)


    # ESTO ES PARA ACTUALIZAR LOS DATOS DE QR EN LA BASE DE DATOS
    curQR = mysql.connection.cursor()
    id_mascota = last_id  # O el ID que desees actualizar

    # Actualiza el campo FotoQR
    curQR.execute("UPDATE ExpedienteMascota SET FotoQR = %s WHERE IDMascota = %s", (image_dataQR, id_mascota))
    mysql.connection.commit()
    curQR.close()


    # Redirigir a la página de éxito
    return redirect(url_for('correct_add', id=last_id, nombre=nombreMascota, colorCSS = colorCSS))

# Enrutamiento expediente agregado
@app.route('/correct_add')
def correct_add():
    id = request.args.get('id')
    mascota = request.args.get('nombre')
    ColorCSS = request.args.get('colorCSS')

    # Recuperar la imagen del registro de la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT FotoMascota FROM expedientemascota WHERE IDMascota = %s", (id,))
    image_data = cur.fetchone()[0]
    cur.close()

    # Convertir los datos de imagen a una cadena base64 para mostrar en HTML
    image_base64 = "data:image/png;base64," + base64.b64encode(image_data).decode('utf-8')

    return render_template('correctExpediente.html', id=id, mascota=mascota, image_base64=image_base64, colorCSS = ColorCSS)


# Enrutamiento obtener ID expediente por input
@app.route('/selectExp', methods=['GET', 'POST'])
def selectExp():
    return render_template('selectExpedienteInt.html')

# Enrutamiento obtener ID expediente por SCANNER
@app.route('/scannerExp', methods=['GET', 'POST'])
def scannerExp():
    return render_template('scannerExp.html')

# Ruta para obtener los datos de expediente de mascota
@app.route('/showExp', methods=['POST'])
def showExp():
    vet_key = request.form['VetKey']
    
    # Consultar la base de datos usando VetKey
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ExpedienteMascota WHERE IDMascota = %s", (vet_key,))
    data = cur.fetchone()
    cur.close()

    if data:

        # Convertir la imagen a base64 de Mascota para mostrarla
        imageMascota_data = data[7]  # Asumiendo que ImageNombre es segundo campo a partir del cero XD
        imageMascota_base64 = "data:image/png;base64," + base64.b64encode(imageMascota_data).decode('utf-8')

        # Convertir la imagen QR a base64 de Mascota para mostrarla
        imageQR_data = data[18]  # Asumiendo que ImageNombre es segundo campo a partir del cero XD
        imageQR_base64 = "data:image/png;base64," + base64.b64encode(imageQR_data).decode('utf-8')

        return render_template('showExpediente.html', idMascota=data[0], nombreMascota=data[1], sexo=data[2], especie =data[3], raza=data[4], edad=data[5], detalles=data[6],peso=data[8], imageMascota_base64=imageMascota_base64,imageQR_base64=imageQR_base64,)
    else:
        return render_template('404error.html') 


# Ruta para obtener los datos de expediente de mascota - HISTORIAL MEDICO
@app.route('/showExpHistorialMedico', methods=['POST'])
def showExpHistorialMedico():
    vet_key = request.form['VetKey']
    
    # Consultar la base de datos usando VetKey
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ExpedienteMascota WHERE IDMascota = %s", (vet_key,))
    data = cur.fetchone()
    cur.close()
    if data:
        # Convertir la imagen a base64 de Mascota para mostrarla
        imageMascota_data = data[7]  # Asumiendo que ImageNombre es segundo campo a partir del cero XD
        imageMascota_base64 = "data:image/png;base64," + base64.b64encode(imageMascota_data).decode('utf-8')
        enfermedades = data[9].split(', ') if data and data[9] else []
        vacunas = data[11].split(', ') if data and data[11] else []
        examenes = data[12].split(', ') if data and data[12] else []

        return render_template('showExpedienteHistorialMedico.html', idMascota=data[0],nombreMascota=data[1],enfermedades=enfermedades,esterilizado=data[10],vacunas=vacunas,examenes=examenes,examenesObservacion=data[13],desparasitaciones=data[14], imageMascota_base64=imageMascota_base64,)
    else:
        return render_template('404error.html') 
   

# Ruta para obtener los datos de expediente de mascota - CITA MEDICA
@app.route('/showExpCitaMedica', methods=['POST'])
def showExpCitaMedica():
    vet_key = request.form['VetKey']
    
    # Consultar la base de datos usando VetKey
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ExpedienteMascota WHERE IDMascota = %s", (vet_key,))
    data = cur.fetchone()
    cur.close()
    if data:
        # Convertir la imagen a base64 de Mascota para mostrarla
        imageMascota_data = data[7]  # Asumiendo que ImageNombre es segundo campo a partir del cero XD
        imageMascota_base64 = "data:image/png;base64," + base64.b64encode(imageMascota_data).decode('utf-8')

        return render_template('showExpedienteCitaMedica.html', idMascota=data[0],nombreMascota=data[1],ultimacita=data[15],descultimacita=data[19],proximacita=data[16],descproximacita=data[20],nombreveterinario=data[21], imageMascota_base64=imageMascota_base64,)
    else:
        return render_template('404error.html') 
    

# Ruta para obtener los datos de expediente de mascota - PROPIETARIO
@app.route('/showExpPropietario', methods=['POST'])
def showExpPropietario():
    vet_key = request.form['VetKey']
    
    # Consultar la base de datos usando VetKey
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ExpedienteMascota WHERE IDMascota = %s", (vet_key,))
    data = cur.fetchone()
    cur.close()

    if data:
        # pedir DUI propietario
        DUIProp = data[17]
        # Consultar la base de datos usando DUIProp
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Propietario WHERE DUI = %s", (DUIProp,))
        dataProp = cur.fetchone() # almacena los datos de Propietarios
        cur.close()

        # Convertir la imagen a base64 de Mascota para mostrarla
        imageMascota_data = data[7]  # Asumiendo que ImageNombre es segundo campo a partir del cero XD
        imageMascota_base64 = "data:image/png;base64," + base64.b64encode(imageMascota_data).decode('utf-8')

        # Convertir la imagen a base64 de Propietario para mostrarla
        imageProp_data = dataProp[2]  # Asumiendo que ImageNombre es segundo campo a partir del cero XD
        imageProp_base64 = "data:image/png;base64," + base64.b64encode(imageProp_data).decode('utf-8')

        return render_template('showExpedientePropietario.html', idMascota=data[0], nombreMascota=data[1], dui=dataProp[0], nombrePropietario=dataProp[1], telefono=dataProp[3], direccion=dataProp[4], correo=dataProp[5], imageMascota_base64=imageMascota_base64, imageProp_base64=imageProp_base64,)
    else:
        return render_template('404error.html') 




# Enrutamiento obtener ID expediente por input
@app.route('/selectProp', methods=['GET', 'POST'])
def selectProp():
    return render_template('selectPropietario.html')

# Ruta para mostrar datos a partir de DUI
@app.route('/showByDUI', methods=['POST'])
def showByDUI():
    prop_key = request.form['PropKey']
    
    # Consultar la base de datos usando PropKey
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ExpedienteMascota WHERE DUI = %s", (prop_key,))
    expedientes = cur.fetchall()  # Obtener todos los registros
    cur.close()

    if expedientes:
        mascotas_data = []
        for expediente in expedientes:
            # Convertir la imagen a base64 de Mascota para mostrarla
            imageMascota_data = expediente[7]  # Asumiendo que FotoMascota es el octavo campo
            imageMascota_base64 = "data:image/png;base64," + base64.b64encode(imageMascota_data).decode('utf-8')

            # Almacenar los datos necesarios en un diccionario
            mascotas_data.append({
                'nombre_mascota': expediente[1],  # NombreMascota
                'especie': expediente[3],          # Especie
                'raza': expediente[4],             # Raza
                'foto_mascota': imageMascota_base64  # FotoMascota
            })

        return render_template('showByDUI.html', mascotas=mascotas_data)
    else:
        return render_template('404error.html') 


# Enrutamiento obtener especie por input
@app.route('/selectEspecie', methods=['GET', 'POST'])
def selectEspecie():
    return render_template('selectEspecie.html')

# Ruta para mostrar a partir de la especie
@app.route('/showByEspecie', methods=['POST'])
def showByEspecie():
    especie = request.form['especie']  # Obtener la especie del formulario
    
    # Consultar la base de datos para la especie seleccionada
    cur = mysql.connection.cursor()
    cur.execute("SELECT NombreMascota, Especie, Raza, UltimaCita, ProxCita, FotoMascota FROM ExpedienteMascota WHERE Especie = %s", (especie,))
    expedientes = cur.fetchall()  # Obtener todos los registros
    cur.close()

    if expedientes:
        mascotas_data = []
        for expediente in expedientes:
            # Convertir la imagen a base64 de Mascota para mostrarla
            imageMascota_data = expediente[5]  # Asumiendo que FotoMascota es el sexto campo
            imageMascota_base64 = "data:image/png;base64," + base64.b64encode(imageMascota_data).decode('utf-8')

            # Almacenar los datos necesarios en un diccionario
            mascotas_data.append({
                'nombre_mascota': expediente[0],  # NombreMascota
                'especie': expediente[1],          # Especie
                'raza': expediente[2],             # Raza
                'ultima_cita': expediente[3],      # UltimaCita
                'prox_cita': expediente[4],        # ProxCita
                'foto_mascota': imageMascota_base64  # FotoMascota
            })

        return render_template('showByEspecie.html', mascotas=mascotas_data, especie=especie)
    else:
        return render_template('404error.html') 
    
    
chat_history = []
avatars = {'user': 'user-avatar.png', 'bot': 'bot-avatar.png'}
questions = [
    "¿ Cuál es el nombre del animal ?",
    "¿ Qué especie es (perro, gato, etc...) ?",
    "¿ Cuál es la edad del animal ?",
    "¿ Cuál es el sexo del animal (masculino/femenino) ?",
    "Describe los síntomas.",
    "¿ Tiene antecedentes médicos ?"
]
current_question = 0
responses = {}
is_generating = False  # Variable para controlar si se está generando una respuesta

# Definición de respuestas alternativas ampliadas
responses_map = {
    'yes': ['sí', 'si', 'quiero una nueva consulta', 'me gustaría continuar', 
            'sí, por favor', 'claro', 'adelante', 'por supuesto', 
            'sí, quiero más', 'continúa'],
    'no': ['no', 'ya no quiero seguir hablando', 'gracias, eso es todo', 
           'no gracias', 'no quiero continuar', 'no, eso es suficiente'],
    'talk_to_vet': ['hablar con un veterinario', 'necesito hablar con un veterinario', 
                    'quiero consultar a un veterinario', 'deseo hablar con un veterinario',
                    'quiero ver a un veterinario', 'hablar con un experto']
}

@app.route("/chatbot", methods=["GET", "POST"])
def chat():
    global current_question, responses, chat_history, is_generating

    if request.method == "POST":
        if "reset" in request.form:
            chat_history.clear()
            responses.clear()
            current_question = 0
            is_generating = False  # Reiniciar el estado al limpiar la conversación
            return redirect(url_for("chat"))

        user_input = request.form.get("user_input").strip().lower()  # Normalizar entrada

        # Si estamos generando una respuesta, ignorar la entrada del usuario
        if is_generating:
            return redirect(url_for("chat"))

        chat_history.append({'sender': 'user', 'text': user_input, 'avatar': avatars['user']})

        if current_question >= len(questions):
            if match_response(user_input, responses_map['yes']):
                current_question = 0
                responses.clear()
                chat_history.append({'sender': 'bot', 'text': questions[current_question], 'avatar': avatars['bot']})
            elif match_response(user_input, responses_map['no']):
                chat_history.append({'sender': 'bot', 
                                     'text': "Gracias por usar el asistente veterinario. ¡Hasta la próxima!", 
                                     'avatar': avatars['bot']})
                chat_history.append({'sender': 'bot', 
                                     'text': "Si necesitas ayuda nuevamente, no dudes en volver.", 
                                     'avatar': avatars['bot']})
            elif match_response(user_input, responses_map['talk_to_vet']):
                chat_history.append({'sender': 'bot', 
                                     'text': "Por favor, contacta a un veterinario para asistencia directa.", 
                                     'avatar': avatars['bot']})
                chat_history.append({'sender': 'bot', 
                                     'text': "Si tienes más preguntas sobre tu mascota, aquí estoy para ayudarte.", 
                                     'avatar': avatars['bot']})
            else:
                # Mensaje claro para opciones inválidas
                chat_history.append({'sender': 'bot', 
                                     'text': "Lo siento, no entendí eso. Por favor responde con:\n- *sí* para otra consulta\n- *no* para salir\n- *hablar con un veterinario* para asistencia directa.", 
                                     'avatar': avatars['bot']})

        else:
            responses[questions[current_question]] = user_input
            current_question += 1
            if current_question < len(questions):
                chat_history.append({'sender': 'bot', 'text': questions[current_question], 'avatar': avatars['bot']})
            else:
                is_generating = True  # Indicar que se está generando una respuesta
                time.sleep(2)  # Simular tiempo de procesamiento
                final_response = generar_respuesta_veterinaria(
                    responses[questions[0]], responses[questions[1]],
                    responses[questions[2]], responses[questions[3]],
                    responses[questions[4]], responses[questions[5]]
                )
                chat_history.append({'sender': 'bot', 'text': final_response, 'avatar': avatars['bot']})
                chat_history.append({'sender': 'bot', 
                                     'text': "¿ Qué te gustaría hacer ahora ? Escribe:\n (sí) para otra consulta\n (no) para salir\n (hablar con un veterinario).", 
                                     'avatar': avatars['bot']})
                is_generating = False  # Reiniciar el estado después de generar la respuesta

        return redirect(url_for("chat"))

    if current_question == 0 and not chat_history:
        chat_history.append({'sender': 'bot', 
                             'text': "Hola, soy tu asistente veterinario Con Inteligencia Artificial Estoy aquí para proporcionarte recomendaciones y consejos sobre tratamientos medicos . ¡Comencemos!", 
                             'avatar': avatars['bot']})
        chat_history.append({'sender': 'bot', 
                             'text': questions[current_question], 
                             'avatar': avatars['bot']})

    return render_template("chatbot.html", chat_history=chat_history)

def match_response(user_input, valid_responses):
    """Función que verifica si la entrada del usuario coincide con alguna respuesta válida o busca similitudes."""
    # Verificar coincidencias exactas
    for response in valid_responses:
        if response in user_input:
            return True
    
    # Si no hay coincidencias exactas, buscar similitudes
    similar_responses = difflib.get_close_matches(user_input, valid_responses, n=1, cutoff=0.6)
    if similar_responses:
        print(f"Coincidencia similar encontrada: {similar_responses[0]}")  # Para depuración
        return True
    
    return False

if __name__ == '__main__':
    app.run(debug=True)

#if __name__ == "__main__":
   #app.run(host='0.0.0.0', port=5000)


# (c) 2024 Eduardo Enrique Rodríguez Rodríguez

#Contacto

#Nombre: Eduardo Enrique Rodríguez Rodríguez
#Email: eduardorrodriguez.dev@gmail.com