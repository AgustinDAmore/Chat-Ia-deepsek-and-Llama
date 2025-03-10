import tkinter as tk
from tkinter import scrolledtext, filedialog
from openai import OpenAI
import threading
import re  # Para usar expresiones regulares
import Api_Keys
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Variables globales
system_content = "You are a helpful assistant"
rol_actual = "Asistente"
modo_oscuro = False  # Variable para rastrear el modo actual
asistente_actual = "DeepSeek"  # Variable para rastrear el asistente actual
system_modelIA = "deepseek-chat"

# Colores para el modo claro y oscuro
colores_claro = {
    "fondo": "white",
    "texto": "black",
    "boton_fondo": "lightgray",
    "boton_texto": "black",
    "entrada_fondo": "white",
    "entrada_texto": "black",
    "salida_fondo": "white",
    "salida_texto": "black",
}

colores_oscuro = {
    "fondo": "black",
    "texto": "white",
    "boton_fondo": "gray",
    "boton_texto": "white",
    "entrada_fondo": "gray",
    "entrada_texto": "white",
    "salida_fondo": "black",
    "salida_texto": "white",
}

# Función para cambiar entre modo oscuro y claro
def cambiar_modo():
    global modo_oscuro
    modo_oscuro = not modo_oscuro  # Alternar entre True y False
    colores = colores_oscuro if modo_oscuro else colores_claro

    # Aplicar colores a los widgets
    ventana.config(bg=colores["fondo"])
    etiqueta_rol.config(bg=colores["fondo"], fg=colores["texto"])
    etiqueta_asistente.config(bg=colores["fondo"], fg=colores["texto"])
    salida.config(bg=colores["salida_fondo"], fg=colores["salida_texto"])
    entrada.config(bg=colores["entrada_fondo"], fg=colores["entrada_texto"])
    boton_enviar.config(bg=colores["boton_fondo"], fg=colores["boton_texto"])

# Función que se ejecuta cuando se presiona el botón "Enviar"
def enviar():
    # Obtener el texto del campo de entrada
    texto = entrada.get()
    if texto.strip():  # Verificar que el texto no esté vacío
        # Habilitar el área de texto para insertar el mensaje
        salida.config(state=tk.NORMAL)
        salida.insert(tk.END, f"Tú: {texto}\n")
        salida.insert(tk.END, f"\n")
        salida.insert(tk.END, f"{asistente_actual} {system_modelIA}: Pensando...\n")  # Mensaje temporal
        salida.yview(tk.END)  # Desplazar al final
        salida.config(state=tk.DISABLED)

        # Limpiar el campo de entrada
        entrada.delete(0, tk.END)

        # Llamar a la API en segundo plano
        if(system_modelIA=="imagen-3.0-generate-002"):
            threading.Thread(target=generar_imagenes, args=(texto,)).start()
        else:
            threading.Thread(target=obtener_respuesta, args=(texto,)).start()

# Función para obtener la respuesta de la API
def obtener_respuesta(texto):
    if asistente_actual == "DeepSeek":
        client = OpenAI(api_key=Api_Keys.api_key_deepseek, base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model=system_modelIA,
            messages=[
                {"role": "system", "content": system_content},  # Usar el contenido del sistema actual
                {"role": "user", "content": texto},
            ],
            stream=False
        )
        respuesta = response.choices[0].message.content
    elif asistente_actual == "Llama":
        client = OpenAI(
            api_key=Api_Keys.api_key_llama,  # Reemplaza con tu API key de Llama
            base_url="https://api.llama-api.com/"
        )

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": texto},
            ],
            model=system_modelIA,
            stream=False
        )
        respuesta = response.choices[0].message.content
    elif asistente_actual == "Gemini":
        client = OpenAI(
            api_key=Api_Keys.api_key_gemini,  # Reemplaza con tu API key de Llama
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        response = client.chat.completions.create(
            model=system_modelIA,
            n=1,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": texto},
            ],
        )
        respuesta = response.choices[0].message.content
    # Actualizar la interfaz gráfica con la respuesta
    ventana.after(0, actualizar_interfaz, respuesta)

# Función para generar imágenes con Gemini
def generar_imagenes(texto):
    client = genai.Client(api_key=Api_Keys.api_key_gemini)

    response = client.models.generate_images(
        model=system_modelIA,
        prompt=texto,
        config=types.GenerateImagesConfig(
            number_of_images=4,
        )
    )
    for generated_image in response.generated_images:
        image = Image.open(BytesIO(generated_image.image.image_bytes))
        image.show()
    ventana.after(0, actualizar_interfaz, "Se genearon las imagenes!")
    
# Función para actualizar la interfaz gráfica con la respuesta
def actualizar_interfaz(respuesta):
    salida.config(state=tk.NORMAL)
    # Eliminar el mensaje "Pensando..."
    salida.delete("end-2l", "end-1c")
    # Insertar la respuesta real
    salida.insert(tk.END, f"{asistente_actual} {system_modelIA}: {respuesta}\n")
    # Aplicar formato a las partes que están entre **
    aplicar_formato_negritas()
    salida.yview(tk.END)  # Desplazar al final
    salida.config(state=tk.DISABLED)

# Función para aplicar negritas al texto entre **
def aplicar_formato_negritas():
    # Obtener todo el texto del widget Text
    texto = salida.get("1.0", tk.END)

    # Buscar todas las coincidencias de texto entre **
    coincidencias = list(re.finditer(r"\*\*(.*?)\*\*", texto))

    for match in reversed(coincidencias):  
        inicio = f"1.0 + {match.start()} chars"
        fin = f"1.0 + {match.end()} chars"
        salida.delete(inicio, f"1.0 + {match.start() + 2} chars")  
        salida.delete(f"1.0 + {match.end() - 4} chars", fin) 
        salida.tag_add("negrita", f"1.0 + {match.start()} chars", f"1.0 + {match.end() - 4} chars")
        salida.insert(f"1.0 + {match.end() - 4} chars", " ")

# Función para exportar el chat a un archivo .txt
def exportar_txt():
    # Obtener todo el contenido del área de texto
    contenido = salida.get("1.0", tk.END)
    # Abrir un cuadro de diálogo para guardar el archivo
    archivo = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
        title="Guardar chat como"
    )
    if archivo:  # Si se selecciona un archivo
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido)

# Función para cambiar el contenido del sistema y actualizar la etiqueta del rol
def cambiar_rol(rol):
    global system_content, rol_actual
    roles = {
        "Asistente": "You are a helpful assistant",
        "Filósofo": "Eres un filósofo experto en ética y filosofía moderna. Solo debes responder preguntas relacionadas con la filosofía. Si recibes una consulta que no está relacionada con este tema, debes responder: 'Lo siento, solo puedo responder preguntas relacionadas con la filosofía.'",
        "Programador": "Eres un programador experto en Python y desarrollo de software. Solo debes responder preguntas relacionadas con el desarrollo de software. Si recibes una consulta que no está relacionada con este tema, debes responder: 'Lo siento, solo puedo responder preguntas relacionadas con desarrollo de software.'",
        "Historiador": "Eres un historiador especializado en la historia del siglo XX. Solo debes responder preguntas relacionadas con la historia. Si recibes una consulta que no está relacionada con este tema, debes responder: 'Lo siento, solo puedo responder preguntas relacionadas con historia.'",
    }
    system_content = roles.get(rol, "You are a helpful assistant")  # Actualizar el contenido del sistema
    rol_actual = rol  # Actualizar el rol actual
    etiqueta_rol.config(text=f"Rol actual: {rol_actual}")  # Actualizar la etiqueta en la interfaz
    print(f"Rol cambiado a: {rol}")  # Opcional: Imprimir el rol seleccionado

def cambiar_modeloIA(modeloIA):
    global system_modelIA
    system_modelIA = modeloIA  # Actualizar el modelo de IA actual
    etiqueta_modeloIA.config(text=f"Modelo IA actual: {modeloIA}")  # Actualizar la etiqueta en la interfaz
    actualizar_menu_modeloIA(modeloIA)
    print(f"Modelo IA cambiado a: {modeloIA}")  # Opcional: Imprimir el modelo seleccionado

# Función para cambiar el asistente virtual
def cambiar_asistente(asistente):
    global asistente_actual
    asistente_actual = asistente
    etiqueta_asistente.config(text=f"Asistente actual: {asistente}")  # Actualizar la etiqueta en la interfaz
    print(f"Asistente cambiado a: {asistente}")  # Opcional: Imprimir el asistente seleccionado

    # Actualizar el menú de modelos de IA según el asistente seleccionado
    if asistente == "DeepSeek":
        cambiar_modeloIA("deepseek-chat")  # Establecer el modelo predeterminado para DeepSeek
    elif asistente_actual == "Llama":
        cambiar_modeloIA("llama3-8b")  # Establecer el modelo predeterminado para Llama
    else:
        cambiar_modeloIA("gemini-2.0-flash")
def actualizar_menu_modeloIA(modeloIA):
    menu_modeloIA.delete(0, tk.END)  # Limpiar el menú existente

    if asistente_actual == "DeepSeek":
        menu_modeloIA.add_command(label="deepseek-chat", command=lambda: cambiar_modeloIA("deepseek-chat"))
    elif asistente_actual == "Llama":
        menu_modeloIA.add_command(label="llama3-8b", command=lambda: cambiar_modeloIA("llama3-8b"))
        menu_modeloIA.add_command(label="llama3.2-3b", command=lambda: cambiar_modeloIA("llama3.2-3b"))
        menu_modeloIA.add_command(label="llama3-70b", command=lambda: cambiar_modeloIA("llama3-70b"))
        menu_modeloIA.add_command(label="llama3.1-8b", command=lambda: cambiar_modeloIA("llama3.1-8b"))
    else:
        menu_modeloIA.add_command(label="gemini-2.0-flash", command=lambda: cambiar_modeloIA("gemini-2.0-flash"))
        menu_modeloIA.add_command(label="gemini-1.5-flash", command=lambda: cambiar_modeloIA("gemini-1.5-flash"))
        menu_modeloIA.add_command(label="Generador de imagen", command=lambda: cambiar_modeloIA("imagen-3.0-generate-002"))

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Chat con DeepSeek y Llama")

# Configurar el sistema de grid para que sea responsive
ventana.grid_columnconfigure(0, weight=1)  # La columna 0 se expandirá
ventana.grid_rowconfigure(0, weight=1)     # La fila 0 se expandirá

# Crear un menú en la parte superior
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

# Crear un menú "Archivo" con una opción "Exportar TXT"
menu_archivo = tk.Menu(barra_menu, tearoff=0)
menu_archivo.add_command(label="Exportar TXT", command=exportar_txt)
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

# Crear un menú "Rol" con opciones para cambiar el comportamiento del asistente
menu_rol = tk.Menu(barra_menu, tearoff=0)
menu_rol.add_command(label="Asistente", command=lambda: cambiar_rol("Asistente"))
menu_rol.add_command(label="Filósofo", command=lambda: cambiar_rol("Filósofo"))
menu_rol.add_command(label="Programador", command=lambda: cambiar_rol("Programador"))
menu_rol.add_command(label="Historiador", command=lambda: cambiar_rol("Historiador"))
barra_menu.add_cascade(label="Rol", menu=menu_rol)

# Crear un menú "Modo" para cambiar entre modo oscuro y claro
menu_modo = tk.Menu(barra_menu, tearoff=0)
menu_modo.add_command(label="Cambiar modo", command=cambiar_modo)
barra_menu.add_cascade(label="Modo", menu=menu_modo)

# Crear un menú "Asistente" para cambiar entre DeepSeek y Llama
menu_asistente = tk.Menu(barra_menu, tearoff=0)
menu_asistente.add_command(label="DeepSeek", command=lambda: cambiar_asistente("DeepSeek"))
menu_asistente.add_command(label="Llama", command=lambda: cambiar_asistente("Llama"))
menu_asistente.add_command(label="Gemini", command=lambda: cambiar_asistente("Gemini"))
barra_menu.add_cascade(label="Asistente", menu=menu_asistente)

# Crear un menú "Modelo IA" para cambiar el modelo de IA
menu_modeloIA = tk.Menu(barra_menu, tearoff=0)
menu_modeloIA.add_command(label="deepseek-chat", command=lambda: cambiar_modeloIA("deepseek-chat"))
barra_menu.add_cascade(label="Modelo IA", menu=menu_modeloIA)

# Crear una etiqueta para mostrar el rol actual
etiqueta_rol = tk.Label(ventana, text=f"Rol actual: {rol_actual}", font=("Arial", 10))
etiqueta_rol.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

# Crear una etiqueta para mostrar el asistente actual
etiqueta_asistente = tk.Label(ventana, text=f"Asistente actual: {asistente_actual}", font=("Arial", 10))
etiqueta_asistente.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

# Crear una etiqueta para mostrar el modelo de IA actual
etiqueta_modeloIA = tk.Label(ventana, text=f"Modelo IA actual: {system_modelIA}", font=("Arial", 10))
etiqueta_modeloIA.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")

# Crear un área de texto con scroll para mostrar la salida
salida = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, state=tk.DISABLED)
salida.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")  # sticky="nsew" para que se expanda

# Configurar la etiqueta "negrita" para aplicar formato
salida.tag_configure("negrita", font=("Arial", 10, "bold"))

# Configurar la etiqueta "codigo" para aplicar formato
salida.tag_configure("codigo", font=("Courier", 10), background="#f0f0f0", foreground="black")

# Crear un campo de entrada para escribir
entrada = tk.Entry(ventana)
entrada.grid(row=1, column=0, padx=10, pady=10, sticky="ew")  # sticky

# Crear un botón "Enviar"
boton_enviar = tk.Button(ventana, text="Enviar", command=enviar)
boton_enviar.grid(row=1, column=1, padx=10, pady=10, sticky="ew")  # sticky="ew" para que se expanda horizontalmente

# Iniciar el bucle principal de la ventana
ventana.mainloop()