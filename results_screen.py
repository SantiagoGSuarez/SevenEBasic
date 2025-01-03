import tkinter as tk
import customtkinter as ctk  
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageOps
import matplotlib.image as mpimg
import tensorflow as tf
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
import datetime
from database import create_connection

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


class ResultsScreen(tk.Frame):
    def __init__(self, master, user_data, results):
        super().__init__(master, bg=IFSUL_WHITE)

        self.master = master
        self.user_data = user_data
        self.results = results


        


        self.pack(fill="both", expand=True)
        self.create_widgets()


        # Vincular el evento de cierre de la ventana principal al método on_close
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        

    def create_widgets(self):
        # Banner superior
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

        ctk.CTkButton(top_banner_frame, text="",image=izquierda_image, command=self.go_back, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=10, height=40, corner_radius=10).pack(side="left", padx=10)

        # Frame para el gráfico
        self.chart_frame = tk.Frame(self, bg=IFSUL_GREY)
        self.chart_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.chart_frame.pack_propagate(False)

        # Banner inferior
        bottom_banner_frame = tk.Frame(self, bg=IFSUL_DARK_GREY, height=100, pady=10, padx=35)
        bottom_banner_frame.pack(side="bottom", fill="x")
        


         # Cargar la imagen de fondo del botón desde Resources
        guardar_image = ctk.CTkImage(Image.open("Resources/guardar.png"), size=(35, 35))


        ctk.CTkButton(bottom_banner_frame, text="",image=guardar_image,command=self.save_results, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=120, height=40, corner_radius=10).pack(side="right", padx=10, pady=20)





        # Graficar los resultados de las emociones
        self.plot_results()

    def plot_results(self):
        emotions = ['Ira', 'Disgusto', 'Miedo', 'Feliz', 'Neutral', 'Triste', 'Sorpresa']

        counts = [self.results['percentages'][emotion] for emotion in emotions]

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
            # Comprobar si yval es un número entero
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
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def save_results(self):
        # Obtener el ID del usuario
        user_id = self.user_data.get('idusuario')  # Asume que el ID de usuario está en user_data
        
        # Obtener porcentajes de emociones
        percentages = self.results['percentages']

        # Guardar en la base de datos
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(""" 
            INSERT INTO resultado (idUsuario, fecha_hora, duracion, ira, disgusto, miedo, feliz, neutral, triste, sorpresa) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            self.results['start_time'],
            self.results['formatted_time'],  # Asegúrate de que duration está en segundos o usa el formato necesario
            percentages['Ira'],
            percentages['Disgusto'],
            percentages['Miedo'],
            percentages['Feliz'],
            percentages['Neutral'],
            percentages['Triste'],
            percentages['Sorpresa']
        ))
        conn.commit()
        cursor.close()
        conn.close()

        # Mensaje de confirmación
        messagebox.showinfo("Guardar Resultados", "Los resultados se han guardado correctamente.")
        self.master.show_user_view_screen(self.user_data)

    def go_back(self):
         # Opcionalmente puedes limpiar algo de estado aquí si es necesario
        self.master.is_closing = False  # Reiniciar el estado al ir atrás
        self.master.show_user_view_screen(self.user_data)        
        self.destroy()  # Destruir la pantalla de resultados

    def on_close(self):  # Agregado para manejar el cierre de la ventana
        if messagebox.askokcancel("Cerrar", "¿Estás seguro de que deseas cerrar la aplicación?"):
            tf.keras.backend.clear_session()  # Limpiar la sesión de TensorFlow
            plt.close('all')  # Cerrar cualquier ventana o gráfico activo de Matplotlib
            
            self.master.quit()
            self.master.destroy()