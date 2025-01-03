import tkinter as tk
import customtkinter as ctk  
from tkinter import messagebox, Scrollbar, Canvas, Frame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageOps, ImageTk
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import datetime
from database import create_connection
import tensorflow as tf




# Colores de la paleta de IFSUL
IFSUL_GREEN = "#006400"
IFSUL_LIGHT_GREEN = "#00A36C"
IFSUL_WHITE = "#FFFFFF" #o F4F4F4
IFSUL_DARK_GREY = "#2F4F4F"
IFSUL_BLACK = "#000000"
IFSUL_HOVER = "#04ca88"
IFSUL_GREY = "#EDEDED"
# Tamaño de fuente global
FONT_MAX = ("Helvetica", 19)
FONT_LARGE = ("Helvetica", 16)
FONT_MEDIUM = ("Helvetica", 14)
FONT_SMALL = ("Helvetica", 12)


class ResultScreen(tk.Frame):
    def __init__(self, master, id_resultado, user_data):
        super().__init__(master, bg=IFSUL_WHITE)

        self.master = master
        self.id_resultado = id_resultado
        self.user_data = user_data

        self.result_data = None  # Almacenar los datos del resultado



        self.pack(fill="both", expand=True)

        self.load_result_data()  # Cargar los datos del resultado

        self.create_widgets()


        # Vincular el evento de cierre de la ventana principal al método on_close
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def load_result_data(self):
        conn = create_connection()
        cursor = conn.cursor()

        # Consulta para obtener los detalles del resultado según el id_resultado
        query = """
        SELECT fecha_hora ,duracion, ira, disgusto, miedo, feliz, neutral, triste, sorpresa
        FROM resultado
        WHERE idResultado = %s
        """
        cursor.execute(query, (self.id_resultado,))
        self.result_data = cursor.fetchone()  # Obtener la fila correspondiente
        conn.close()

    def create_widgets(self):
        top_banner_frame = tk.Frame(self, bg=IFSUL_DARK_GREY, height=50, pady=10, padx=35)
        top_banner_frame.pack(side="top", fill="x")


        # Frame para la etiqueta del nombre del administrador, alineada a la derecha
        admin_frame = tk.Frame(top_banner_frame, bg=IFSUL_DARK_GREY)
        admin_frame.pack(side="top", anchor="ne", padx=10, pady=5)  # Colocado en la parte superior derecha

        # Etiqueta del nombre del administrador
        admin_label = tk.Label(admin_frame, text=f"Administrador: {self.master.admin_name}", bg=IFSUL_DARK_GREY, fg=IFSUL_WHITE, font=("Helvetica", 15, "bold"))
        admin_label.pack()


        # Cargar la imagen para el botón de "Retroceder"
        izquierda_image = ctk.CTkImage(Image.open("Resources/izquierda3.png"), size=(35, 35))

        ctk.CTkButton(top_banner_frame, text="",image=izquierda_image, command=self.go_back, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=10, height=40,corner_radius=10).pack(side="left", padx=10)

        # Frame para la fecha y duración
        date_duration_frame = tk.Frame(self, bg=IFSUL_WHITE)
        date_duration_frame.pack(side="top", fill="x", padx=10, pady=10)

        if self.result_data:
            fecha_hora, duracion, *emotion_data = self.result_data

            # Frame para centrar fecha y hora
            center_frame = tk.Frame(date_duration_frame, bg=IFSUL_WHITE)
            center_frame.pack(side="top", expand=True)

            # Etiqueta de fecha y hora centrada
            fecha_label = tk.Label(center_frame, text=f"Fecha y Hora del Análisis Inicial: {fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}", font=FONT_MEDIUM, bg=IFSUL_WHITE)
            fecha_label.pack()

            # Etiqueta de duración alineada a la derecha en el frame principal
            duracion_label = tk.Label(date_duration_frame, text=f"Duración del Análisis: {duracion}", font=FONT_MEDIUM, bg=IFSUL_WHITE)
            duracion_label.pack(side="right", padx=(0, 10))

            self.plot_results(emotion_data)
        else:
            tk.Label(self, text="No se encontraron datos para este análisis.", font=FONT_MEDIUM, bg=IFSUL_WHITE).pack(pady=10)

    def plot_results(self, emotion_data):
        emotions = ['Ira', 'Disgusto', 'Miedo', 'Feliz', 'Neutral', 'Triste', 'Sorpresa']
        counts = emotion_data  # Asumimos que esto corresponde a [ira, disgusto, miedo, feliz, neutral, triste, sorpresa]

        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor(IFSUL_GREY)  # Establece el color de fondo de la figura
        ax.set_facecolor(IFSUL_GREY)          # Establece el color de fondo del eje

        # Colores según las emociones
        colors = ['#FF0000',  # Ira: Rojo
                '#008000',  # Disgusto: Verde
                '#000000',  # Miedo: Negro
                '#FFFF00',  # Feliz: Amarillo
                '#808080',  # Neutral: Gris
                '#0000FF',  # Triste: Azul
                '#FFA500']  # Sorpresa: Naranja


        bars = ax.bar(emotions, counts, color=colors)
        ax.set_xlabel('Emociones')
        ax.set_ylabel('Porcentaje')
        ax.set_title('Resultados del Análisis de Emociones')

        # Añadir los porcentajes encima de cada barra
        for bar in bars:
            yval = bar.get_height()
            if yval.is_integer():
                ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{int(yval)}%', ha='center', va='bottom')
            else:
                ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.3f}%', ha='center', va='bottom')

        # Ruta a las imágenes en la carpeta Resources
        image_paths = {
            'Ira': 'Resources/ira.png',
            'Disgusto': 'Resources/disgusto.png',
            'Miedo': 'Resources/miedo.png',
            'Feliz': 'Resources/felicidad.png',
            'Neutral': 'Resources/neutral.png',
            'Triste': 'Resources/tristeza.png',
            'Sorpresa': 'Resources/sorpresa.png'
        }

        # Colocar imágenes debajo de cada barra
        for i, emotion in enumerate(emotions):
            # Cargar y redimensionar la imagen
            img = Image.open(image_paths[emotion])
            img = ImageOps.fit(img, (40, 40), Image.LANCZOS)  # Redimensionar a 40x40

            # Convertir la imagen a un array de Matplotlib
            img_array = np.array(img)

            # Crear un OffsetImage para manejar el tamaño
            imagebox = OffsetImage(img_array, zoom=1)

            # Ajustar la posición Y para que las imágenes queden debajo de las barras
            ab = AnnotationBbox(imagebox, (i, counts[i] + 12), frameon=False, box_alignment=(0.5, 0.5))


            # Añadir la imagen como anotación al gráfico
            ax.add_artist(ab)

        # Ajustar los márgenes del gráfico para hacer espacio para las imágenes
        ax.set_ylim([0, max(counts) + 19])

        # Crear un canvas para mostrar el gráfico en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)



    def go_back(self):
        self.master.show_view_results_screen(self.user_data)


    def on_close(self):  # Agregado para manejar el cierre de la ventana
        if messagebox.askokcancel("Cerrar", "¿Estás seguro de que deseas cerrar la aplicación?"):
            # Limpiar la sesión de TensorFlow si es necesario
            tf.keras.backend.clear_session()
            plt.close('all')  # Cierra cualquier ventana o gráfico activo de Matplotlib

            self.master.destroy()  # Cerrar la ventana principal
            self.master.quit()  # Salir del mainloop() para finalizar la ejecución correctamente