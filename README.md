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

Se recomienda usar un .env para nstalar las librerias
En caso de no querer hacerlo pasar directamente a la linea 22

Creamos el entorno virtual:
En linux: python3 -m venv nombre_del_entorno
En Windows: python -m venv nombre_del_entorno

Para activarlo
En linux: source nombre_del_entorno/bin/activate
En Windows: nombre_del_entorno\Scripts\activate

Instalamos los paquetes necesarios
pip install openai

Para desactivar el entorno virtual escribimos en ambos SO
deactivate

Explicacion del codigo fuente