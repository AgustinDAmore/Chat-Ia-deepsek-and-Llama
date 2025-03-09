import tkinter as tk
from tkinter import scrolledtext, filedialog
from openai import OpenAI
import threading
import re  # Para usar expresiones regulares
import Api_Keys

# Variables globales
system_content = "You are a helpful assistant"
rol_actual = "Asistente"
modo_oscuro = False  # Variable para rastrear el modo actual
asistente_actual = "DeepSeek"  # Variable para rastrear el asistente actual

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
        salida.insert(tk.END, f"{asistente_actual}: Pensando...\n")  # Mensaje temporal
        salida.yview(tk.END)  # Desplazar al final
        salida.config(state=tk.DISABLED)

        # Limpiar el campo de entrada
        entrada.delete(0, tk.END)

        # Llamar a la API en segundo plano
        threading.Thread(target=obtener_respuesta, args=(texto,)).start()

# Función para obtener la respuesta de la API
def obtener_respuesta(texto):
    if asistente_actual == "DeepSeek":
        client = OpenAI(api_key=Api_Keys.api_key_deepseek, base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model="deepseek-chat",
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
            model="llama3-8b",
            stream=False
        )
        respuesta = response.choices[0].message.content

    # Actualizar la interfaz gráfica con la respuesta
    ventana.after(0, actualizar_interfaz, respuesta)

# Función para actualizar la interfaz gráfica con la respuesta
def actualizar_interfaz(respuesta):
    salida.config(state=tk.NORMAL)
    # Eliminar el mensaje "Pensando..."
    salida.delete("end-2l", "end-1c")
    # Insertar la respuesta real
    salida.insert(tk.END, f"{asistente_actual}: {respuesta}\n")
    # Aplicar formato a las partes que están entre **
    aplicar_formato_negritas()
    salida.yview(tk.END)  # Desplazar al final
    salida.config(state=tk.DISABLED)

# Función para aplicar negritas al texto entre **
def aplicar_formato_negritas():
    # Buscar todas las coincidencias de texto entre **
    texto = salida.get("1.0", tk.END)
    coincidencias = list(re.finditer(r"\*\*(.*?)\*\*", texto))

    # Aplicar formato a cada coincidencia
    for match in coincidencias:
        inicio = f"1.0 + {match.start()} chars"
        fin = f"1.0 + {match.end()} chars"
        salida.tag_add("negrita", inicio, fin)

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
        "Filósofo": "Eres un filósofo experto en ética y filosofía moderna.",
        "Programador": "Eres un programador experto en Python y desarrollo de software.",
        "Historiador": "Eres un historiador especializado en la historia del siglo XX.",
    }
    system_content = roles.get(rol, "You are a helpful assistant")  # Actualizar el contenido del sistema
    rol_actual = rol  # Actualizar el rol actual
    etiqueta_rol.config(text=f"Rol actual: {rol_actual}")  # Actualizar la etiqueta en la interfaz
    print(f"Rol cambiado a: {rol}")  # Opcional: Imprimir el rol seleccionado

# Función para cambiar el asistente virtual
def cambiar_asistente(asistente):
    global asistente_actual
    asistente_actual = asistente
    etiqueta_asistente.config(text=f"Asistente actual: {asistente}")  # Actualizar la etiqueta en la interfaz
    print(f"Asistente cambiado a: {asistente}")  # Opcional: Imprimir el asistente seleccionado

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
barra_menu.add_cascade(label="Asistente", menu=menu_asistente)

# Crear una etiqueta para mostrar el rol actual
etiqueta_rol = tk.Label(ventana, text=f"Rol actual: {rol_actual}", font=("Arial", 10))
etiqueta_rol.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

# Crear una etiqueta para mostrar el asistente actual
etiqueta_asistente = tk.Label(ventana, text=f"Asistente actual: {asistente_actual}", font=("Arial", 10))
etiqueta_asistente.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")

# Crear un área de texto con scroll para mostrar la salida
salida = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, state=tk.DISABLED)
salida.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")  # sticky="nsew" para que se expanda

# Configurar la etiqueta "negrita" para aplicar formato
salida.tag_configure("negrita", font=("Arial", 10, "bold"))

# Crear un campo de entrada para escribir
entrada = tk.Entry(ventana)
entrada.grid(row=1, column=0, padx=10, pady=10, sticky="ew")  # sticky="ew" para que se expanda horizontalmente

# Crear un botón "Enviar"
boton_enviar = tk.Button(ventana, text="Enviar", command=enviar)
boton_enviar.grid(row=1, column=1, padx=10, pady=10, sticky="ew")  # sticky="ew" para que se expanda horizontalmente

# Iniciar el bucle principal de la ventana
ventana.mainloop()