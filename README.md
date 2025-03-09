# 🚀 Proyecto: Integración con APIs de LLM (DeepSeek y Llama)

Este proyecto permite interactuar con las APIs de **DeepSeek** y **Llama** para generar respuestas utilizando modelos de lenguaje avanzados. A continuación, se detallan los pasos para configurar y ejecutar el proyecto.

---

## 📋 Requisitos previos

Antes de comenzar, asegúrate de tener lo siguiente:

1. **Claves de API**:
   - Obtén una clave de API de [Llama](https://console.llamaapi.com/en/dashboard).
   - Obtén una clave de API de [DeepSeek](https://platform.deepseek.com/usage).

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


🖥️ Se recomienda usar un `.env` para instalar las librerías.

```markdown
1.  Crear el entorno virtual

    En Linux:

    ```bash
    python3 -m venv nombre_del_entorno
    ```

    En Windows:

    ```bash
    python -m venv nombre_del_entorno
    ```

2.  Activar el entorno virtual

    En Linux:

    ```bash
    source nombre_del_entorno/bin/activate
    ```

    En Windows:

    ```bash
    nombre_del_entorno\Scripts\activate
    ```

3.  Instalar los paquetes necesarios

    ```bash
    pip install openai
    ```

4.  Desactivar el entorno virtual

    ```bash
    deactivate
    ```

📝 Explicación del código

El proyecto se centra en la integración de dos APIs de modelos de lenguaje: `DeepSeek` y `Llama`. A continuación, se describe brevemente cómo funciona el código:

* **Configuración de las claves de API**:
    * Las claves de API se almacenan en un archivo separado (`Api_Keys.py`) para mantener la seguridad y facilitar su gestión.
* **Uso de un entorno virtual**:
    * Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto y evitar conflictos con otros proyectos.
* **Instalación de dependencias**:
    * Se utiliza `pip` para instalar las librerías necesarias, como `openai`, que facilita la interacción con las APIs de los modelos de lenguaje.
* **Interacción con las APIs**:
    * El código principal del proyecto se encargará de enviar solicitudes a las APIs de DeepSeek y Llama, procesar las respuestas y generar salidas útiles basadas en los modelos de lenguaje.

🚀 Ejecución del proyecto

Una vez configurado el entorno y las claves de API, puedes ejecutar el proyecto para interactuar con las APIs y obtener respuestas generadas por los modelos de lenguaje.

```bash
python main.py