# 🐾 Vet AI - Sistema de Expediente Veterinario

Sistema web de gestión de expedientes veterinarios desarrollado con **Python** y **Flask**, diseñado para digitalizar y facilitar el manejo de información de pacientes veterinarios, propietarios e historiales médicos, integrando inteligencia artificial a través de APIs externas.

> Proyecto desarrollado como parte de la materia de **Inteligencia Artificial** — Universidad Salvadoreña Alberto Masferrer.

## 📋 Descripción

Vet AI permite registrar propietarios y mascotas, generar expedientes con acceso rápido mediante **códigos QR**, y llevar el control de historial médico y citas. El sistema integra la **API de Gemini de Google** para generar recomendaciones veterinarias automáticas a partir de los síntomas y antecedentes registrados de cada paciente, además de contar con un chatbot de apoyo para consultas.

## Funcionalidades principales

- Registro y gestión de propietarios (con foto, DUI, contacto)
- Registro de expedientes veterinarios por mascota y especie
- Generación de **códigos QR** para acceso rápido a cada expediente
- Consulta de expedientes por propietario, especie o DUI
- Historial médico y citas médicas por paciente
- Generación de recomendaciones veterinarias con **IA (API de Gemini)** en base a síntomas y antecedentes
- Chatbot de apoyo integrado
- Manejo de errores personalizados (404)

## Tecnologías utilizadas

- **Backend:** Python, Flask
- **Base de datos:** MySQL (Flask-MySQLdb)
- **IA:** Google Generative AI (Gemini API)
- **Generación de QR:** qrcode, Pillow (PIL)
- **Frontend:** HTML, CSS, JavaScript (Jinja2 templates)
- **Variables de entorno:** python-dotenv

## 📦 Estructura del proyecto

```
Vet-AI-python-project/
├── src/
│   └── static/         # CSS, JS, imágenes, códigos QR generados
│   └── templates/       # Vistas HTML (Jinja2)
├── DB_vet_ai.sql         # Script de la base de datos
├── requirements.txt      # Dependencias del proyecto
└── app.py                # Lógica principal del backend (Flask)
```

## ⚙️ Instalación y uso

1. Clona el repositorio:
   ```bash
   git clone https://github.com/WayoGFX/Vet-AI-python-project.git
   cd Vet-AI-python-project
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv env
   env\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. Crea un archivo `.env` en la raíz del proyecto con tu API Key de Gemini:
   ```
   API_KEY=tu_api_key_de_gemini
   ```

4. Importa la base de datos `DB_vet_ai.sql` en tu servidor MySQL local.

5. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

## 👤 Autor

**Eduardo Enrique Rodríguez Rodríguez**
[LinkedIn](https://www.linkedin.com/in/eduardo-rrodriguez-dev/) · eduardorrodriguez.dev@gmail.com
