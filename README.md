# 🚀 Proyecto: Integración con APIs de LLM (DeepSeek y Llama)

Este proyecto permite interactuar con las APIs de **DeepSeek** y **Llama** para generar respuestas utilizando modelos de lenguaje avanzados. A continuación, se detallan los pasos para configurar y ejecutar el proyecto.

---

## 📋 Requisitos previos

Antes de comenzar, asegúrate de tener lo siguiente:

1. **Claves de API**:
    - Obtén una clave de API de [Llama](https://console.llamaapi.com/en/dashboard).
    - Obtén una clave de API de [DeepSeek](https://platform.deepseek.com/usage).
    - Obtén una clave de API de [Gemini](https://ai.google.dev/gemini-api/docs/api-key).
2. **Python**:
    - Asegúrate de tener Python instalado (versión 3.7 o superior).

---
## 🛠️ Configuración del proyecto

### 1. **Crear el archivo `Api_Keys.py`**
   Crea un archivo llamado `Api_Keys.py` en la raíz del proyecto y añade las claves de API:

   ```python
   # Api_Keys.py
   api_key_deepseek = "Tu_key_API_DeepSeek"
   api_key_llama = "Tu_key_API_Llama"
   api_key_gemini = "Tu_key_API_Gemini"
   ```
---
## 🖥️ Se recomienda usar un .env para instalar las librerias

### 1. **Creamos el entorno virtual:**
        En linux: python3 -m venv nombre_del_entorno
        En Windows: python -m venv nombre_del_entorno

### 2. **Para activar el entorno**
        En linux: source nombre_del_entorno/bin/activate
        En Windows: nombre_del_entorno\Scripts\activate
        
### 3. **Instalamos los paquetes necesarios**
        pip install openai

### 4. **Para desactivar el entorno virtual escribimos en ambos SO**
        deactivate

---
##  🧑‍💻 Interfaz de usuario

![alt text](image.png)

>La interfaz es responsive y simple de usar
### **Menu superior**
>Contiene 4 opciones
- **Archivo**
    - **Exportar TXT**
        Al seleccionar estaopcion nos permite exportar toda la conversacion en un txt para su posterior lectura
- **Rol**
    En dicha función, podemos usar roles pre-cargados. Estos roles permiten brindar contexto a la pregunta para que esta sea lo más precisa posible. Por defecto, está programado con 4 roles:

    - **Asistente**:  
    Este es el rol por defecto de todos los asistentes.

    - **Filósofo**:  
    Rol de muestra para preguntas relacionadas con filosofía.

    - **Programador**:  
    Rol de muestra para preguntas relacionadas con programación y tecnología.

    - **Historiador**:  
    Rol de muestra para preguntas relacionadas con historia y eventos pasados.

- **Modo**
    - **Cambiar modo**
    Permite cambiar la interfaz 
    entre blanco y oscuro

- **Asistente**
    Permite cambiar entre las dos IA
    - **DeepSeek**
    - **Llama**
    - **Gemini**

- **Modelo IA**
    - Dependiendo el Asistente seleccionado los modelos disponibles

> Para generar imagenes debemos seleccionar el Asistente "Gemini"
> luego en Modelo IA "Generador de imagen"
> describe la imagen que quieres generar y pulse "Enviar"
---
### **Menu inferior**
- **Entrada de texto**
    Permite el ingreso de texto
- **Boton Enviar**
    Una vez redactado el mensaje de debe precionar
    este boton para enviar el mensaje

>Debajo de la Entrda de texto
>Se muestra el estado actual del chat

>Rol actual: **muestra el nombre del rol activo**

>Asistente actual: **muestra el nombre de IA activa**

>Modelo IA: **Modelo de IA activa**

---
##  🔧 Perzonalizar el codigo

### **1. def cambiar_rol(rol):**

### **1.a. Crear nuevos Roles**
    roles = {
        "Asistente": "You are a helpful assistant",
        "Filósofo": "Eres un filósofo experto en ética y filosofía moderna. ...",
        "Programador": "Eres un programador experto en Python y desarrollo de software. ...",
        "Historiador": "Eres un historiador especializado en la historia del siglo XX. ...",
    }
>Vemos que la variable roles es un diccionario donde la calve es el nombre del rol
>y el valor es como se debe comportar. siguiendo dicho formato podemos crear todos los roles que quisieramos

    roles = {
        "Asistente": "You are a helpful assistant",
        "Filósofo": "Eres un filósofo experto en ética y filosofía moderna. ...",
        "Programador": "Eres un programador experto en Python y desarrollo de software. ...",
        "Historiador": "Eres un historiador especializado en la historia del siglo XX. ...",
        "Nuevo rol": "Aqui agregamos el tema del cual es 'especialista' ...",
    }
> ⚠️ **¡Atención!** 
> Es necesario agregarlo tambien en menu_rol para que asi aparezca el nuevo rol en el menu desplegable

### **2. def actualizar_menu_modeloIA()**
    Ejemplo de como agregar un nuevo modeloIA

    menu_modeloIA.add_command(label="llama3.1-8b", command=lambda: cambiar_modeloIA("llama3.1-8b"))
    label = "texto que aparece en el menu desplegable" 
    cambiar_modeloIA = "Modelo de la IA extraido de la documentacion de cada API"

> ⚠️ **¡Atención!** 
> Cada menu_modeloIA se tiene que agregar en cada IF de la IA correspondiente
> Para que funcione y que aparezca en la lista de Modelos IA de la interfaz