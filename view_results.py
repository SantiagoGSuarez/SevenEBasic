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


class ViewResultsScreen(tk.Frame):
    def __init__(self, master, user_data):
        super().__init__(master, bg=IFSUL_WHITE)

        self.master = master
        self.user_data = user_data
        self.emotion_images = self.load_emotion_images()
        self.is_active = True  # Bandera para verificar si la ventana está activa


        


        self.pack(fill="both", expand=True)
        self.create_widgets()


        # Vincular el evento de cierre de la ventana principal al método on_close
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        

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

        ctk.CTkButton(top_banner_frame, text="",image=izquierda_image ,command=self.go_back, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=10, height=40, corner_radius=10).pack(side="left", padx=10)

        user_label = tk.Label(self, text=f"Análisis del Usuario: {self.user_data['nome']} {self.user_data['sobrenome']}", font=("Helvetica", 16, "bold"), bg=IFSUL_WHITE)
        user_label.pack(pady=20)

        # Frame centralizado
        center_frame = tk.Frame(self, bg=IFSUL_WHITE)
        center_frame.pack(fill="both", expand=True)

        # Canvas y Scrollbar para el scrollable_frame
        self.canvas = Canvas(center_frame, bg=IFSUL_WHITE)
        self.scrollbar = Scrollbar(center_frame, orient="vertical", command=self.canvas.yview)

        # Frame que contendrá el contenido scrollable
        self.scrollable_frame = Frame(self.canvas, bg=IFSUL_GREY)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Crear una ventana dentro del canvas
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")

        # Empaquetar el canvas y scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Llamar a load_results después de crear el scrollable_frame
        self.load_results(self.scrollable_frame)

        # Manejar el scroll con el mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        # Vincular el evento de redimensionamiento de la ventana
        self.master.bind("<Configure>", self.on_window_resize)

    def on_window_resize(self, event):
        if self.is_active and self.canvas and self.window_id:
            try:
                self.canvas.itemconfig(self.window_id, width=self.canvas.winfo_width())
            except tk.TclError:
                pass

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def load_results(self, parent_frame):
        conn = create_connection()
        cursor = conn.cursor()

        query = """
        SELECT idResultado, ira, disgusto, miedo, feliz, neutral, triste, sorpresa
        FROM resultado
        WHERE idUsuario = %s
        ORDER BY idResultado DESC
        """
        cursor.execute(query, (self.user_data['idusuario'],))
        resultados = cursor.fetchall()

        if not resultados:
            no_results_label = tk.Label(parent_frame, text="No hay análisis disponibles.", font=FONT_MEDIUM, bg=IFSUL_GREY)
            no_results_label.pack(pady=20)
            return

        for idx, row in enumerate(resultados, start=1):
            id_resultado, ira, disgusto, miedo, feliz, neutral, triste, sorpresa = row

            result_frame = tk.Frame(parent_frame, bg=IFSUL_GREY, pady=10, padx=10)
            result_frame.pack(fill="x", pady=5)

            inner_frame = tk.Frame(result_frame, bg=IFSUL_GREY)
            inner_frame.pack(side="top", fill="x", padx=10, expand=True)

            emotions = [
                ("ira", ira), ("disgusto", disgusto), ("miedo", miedo), 
                ("felicidad", feliz), ("neutral", neutral), ("tristeza", triste), ("sorpresa", sorpresa)
            ]

            tk.Label(inner_frame, text=f"{idx}.", font=FONT_MEDIUM, bg=IFSUL_GREY).pack(side="left", padx=10)

            for col, (emotion_name, emotion_value) in enumerate(emotions):
                emotion_frame = tk.Frame(inner_frame, bg=IFSUL_GREY)
                emotion_frame.pack(side="left", padx=5, expand=True)

                img_label = tk.Label(emotion_frame, image=self.emotion_images[emotion_name], bg=IFSUL_GREY)
                img_label.pack(side="top")

                percentage_label = tk.Label(emotion_frame, text=f"{emotion_value:.2f}%", font=FONT_MEDIUM, bg=IFSUL_GREY)
                percentage_label.pack(side="top")

                emotion_name_label = tk.Label(emotion_frame, text=emotion_name.capitalize(), font=FONT_MEDIUM, bg=IFSUL_GREY)
                emotion_name_label.pack(side="top")

            buttons_frame = tk.Frame(inner_frame, bg=IFSUL_GREY)
            buttons_frame.pack(side="right")

            
            ver_image = ctk.CTkImage(Image.open("Resources/ver.png"), size=(28, 28))

            ver_btn = ctk.CTkButton(buttons_frame, text="",image=ver_image, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=10, height=40, corner_radius=10, command=lambda rid=id_resultado: self.master.show_result_screen(rid, self.user_data))
            ver_btn.pack(side="left", padx=10)



            eliminar_image = ctk.CTkImage(Image.open("Resources/eliminar.png"), size=(30, 30))

            eliminar_btn = ctk.CTkButton(buttons_frame, text="",image=eliminar_image, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=10, height=40, corner_radius=10,
                                    command=lambda rid=id_resultado: self.eliminar_resultado(rid))
            eliminar_btn.pack(side="left", padx=10)

        conn.close()

    def load_emotion_images(self):
        emotions = ["disgusto", "felicidad", "ira", "miedo", "neutral", "sorpresa", "tristeza"]
        images = {}
        for emotion in emotions:
            img = Image.open(f"Resources/{emotion}.png")
            img_resized = img.resize((40, 40), Image.LANCZOS)
            images[emotion] = ImageTk.PhotoImage(img_resized)
        return images
    

    def show_result_screen(self):
        # Llama al método de App para abrir la ventana ResultScreen
        self.master.show_result_screen(self.master.user_data)


    def eliminar_resultado(self, id_resultado):
        if messagebox.askokcancel("Eliminar", "¿Estás seguro de que deseas eliminar este resultado?"):
            conn = create_connection()
            cursor = conn.cursor()
            delete_query = "DELETE FROM resultado WHERE idResultado = %s"
            cursor.execute(delete_query, (id_resultado,))
            conn.commit()
            conn.close()
            self.refresh_screen()

    def refresh_screen(self):
        self.is_active = False  # Marcar como no activa
        self.master.unbind("<Configure>")
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
        self.is_active = True  # Marcar como activa de nuevo
        self.master.bind("<Configure>", self.on_window_resize)


    def go_back(self):
        self.is_active = False  # Marcar como no activa antes de ir hacia atrás

        self.master.show_user_view_screen(self.user_data)


    def on_close(self):  # Agregado para manejar el cierre de la ventana
        if messagebox.askokcancel("Cerrar", "¿Estás seguro de que deseas cerrar la aplicación?"):
            # Limpiar la sesión de TensorFlow si es necesario
            tf.keras.backend.clear_session()
            self.master.destroy()  # Cerrar la ventana principal
            self.master.quit()  # Salir del mainloop() para finalizar la ejecución correctamente