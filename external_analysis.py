import tkinter as tk
import customtkinter as ctk  
from tkinter import messagebox
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from PIL import ImageGrab
from collections import defaultdict
import datetime
from collections import deque


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

# Lista de emociones
emotions = ['Ira', 'Disgusto', 'Miedo', 'Feliz', 'Neutral', 'Triste', 'Sorpresa']

# Carga el modelo entrenado
model = tf.keras.models.load_model('ENTRENAMIENTODEFINITIVO_REFORZADO_48x48_GRAYSCALE.h5')

class TransparentScreenCapture:
    def __init__(self, on_selection):
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        self.selection = None
        self.on_selection = on_selection

        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)  # Hacer la ventana semi-transparente
        self.root.attributes("-topmost", True)
        self.root.configure(bg='black')
        self.root.overrideredirect(True)  # Quitar bordes

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', fill='', width=2)

    def on_drag(self, event):
        cur_x = event.x
        cur_y = event.y
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        self.selection = self.canvas.coords(self.rect_id)
        self.root.quit()  # Cierra el bucle principal de la ventana
        self.root.destroy()  # Destruye la ventana completamente
        self.on_selection(self.selection)  # Llama a la función con la selección

class ExternalAnalysisScreen(tk.Frame):
    def __init__(self, master, user_data):
        super().__init__(master, bg=IFSUL_WHITE)
        self.master = master
        self.user_data = user_data

        self.capture_coords = None
        self.running = False

        self.emotion_counts = defaultdict(int)  # Inicializa el conteo de emociones
        self.start_time = None  # Para el conteo de tiempo
        self.elapsed_time_var = tk.StringVar(value="00:00:00")  # Variable para el tiempo transcurrido
       
        # Agregar el historial de predicciones
        self.history = deque(maxlen=10)

        self.create_widgets()

    def create_widgets(self):
        # Configurar la cuadrícula
        self.grid_rowconfigure(0, weight=0)  # Fila para el banner superior
        self.grid_rowconfigure(1, weight=1)  # Fila para la imagen
        self.grid_rowconfigure(2, weight=0)  # Fila para la etiqueta de emoción
        self.grid_rowconfigure(3, weight=0)  # Fila para el banner inferior
        self.grid_columnconfigure(0, weight=1)

        # Frame para la parte superior
        top_banner_frame = tk.Frame(self, bg=IFSUL_DARK_GREY, height=50, pady=10, padx=35)
        top_banner_frame.grid(row=0, column=0, sticky="ew")


        # Frame para la etiqueta del nombre del administrador, alineada a la derecha
        admin_frame = tk.Frame(top_banner_frame, bg=IFSUL_DARK_GREY)
        admin_frame.pack(side="top", anchor="ne", padx=10, pady=5)  # Colocado en la parte superior derecha

        # Etiqueta del nombre del administrador
        admin_label = tk.Label(admin_frame, text=f"Administrador: {self.master.admin_name}", bg=IFSUL_DARK_GREY, fg=IFSUL_WHITE, font=("Helvetica", 15, "bold"))
        admin_label.pack()

        # Cargar la imagen para el botón de "Retroceder"
        izquierda_image = ctk.CTkImage(Image.open("Resources/izquierda3.png"), size=(35, 35))

        ctk.CTkButton(top_banner_frame, text="",image=izquierda_image, command=self.go_back, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=10, height=40, corner_radius=10).pack(side="left", padx=10)

        # Frame para la imagen
        self.video_frame = tk.Frame(self, bg=IFSUL_WHITE)
        self.video_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Label para mostrar la imagen
        self.vid_label = tk.Label(self.video_frame)
        self.vid_label.pack(fill="both", expand=True)

        # Etiqueta para mostrar la emoción detectada
        self.emotion_label = tk.Label(self, text="", fg="red" ,bg=IFSUL_WHITE, font=FONT_MEDIUM)
        self.emotion_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="ew")


        # Label para mostrar el tiempo transcurrido
        self.elapsed_time_label = tk.Label(self, textvariable=self.elapsed_time_var, bg=IFSUL_WHITE, font=FONT_MEDIUM)
        self.elapsed_time_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="ew")


        # Frame para el banner inferior con botones
        banner_frame = tk.Frame(self, bg=IFSUL_DARK_GREY, height=100, pady=10, padx=35)
        banner_frame.grid(row=4, column=0, sticky="ew")

        button_frame = tk.Frame(banner_frame, bg=IFSUL_DARK_GREY)
        button_frame.pack(pady=20)


        # Cargar la imagen para el botón de "Retroceder"
        play_image = ctk.CTkImage(Image.open("Resources/play.png"), size=(35, 35))
        # Cargar la imagen para el botón de "Retroceder"
        detener_image = ctk.CTkImage(Image.open("Resources/detener.png"), size=(35, 35))


        # Botones "Iniciar" y "Detener"
        self.start_button = ctk.CTkButton(button_frame, text="",image=play_image, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=120, height=40, command=self.start_analysis)
        self.stop_button = ctk.CTkButton(button_frame, text="",image=detener_image, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=120, height=40, command=self.stop_analysis)

        self.start_button.pack(side="left", padx=(0, 20))
        self.stop_button.pack(side="left", padx=(20, 0))

    def start_analysis(self):
        if self.running:
            return

        if self.capture_coords is None:
            TransparentScreenCapture(self.on_selection).root.mainloop()
        else:
            self.running = True

            self.start_time = datetime.datetime.now()  # Guarda el tiempo de inicio
            self.update_elapsed_time()  # Comienza el conteo del tiempo
           
            self.process_frame()

    def stop_analysis(self):
        if not self.running:
            return

        self.running = False
        self.vid_label.config(image='')  # Limpiar la imagen en el label
        self.emotion_label.config(text="")  # Ocultar la etiqueta de emoción

        if hasattr(self, 'face_mesh'):
            self.face_mesh.close()
            del self.face_mesh

        # Calcular y guardar resultados
        results = self.calculate_percentages()  # Llama a la función para calcular porcentajes

        self.capture_coords = None
        # Añadimos el tiempo en formato correcto a los resultados
        results['formatted_time'] = self.elapsed_time_var.get()
        results['start_time'] = self.start_time  # Agregamos el start_time a los resultados



        # Llamar a la pantalla de resultados
        self.master.show_results_screen(self.user_data, results)  # Abre la ventana de resultados

    def calculate_percentages(self):
        # Calcular la duración total
        duration = self.elapsed_time_var.get()  # Asegúrate de tener esta variable en tu clase
        # Convertir duración a segundos
        hours, minutes, seconds = map(int, duration.split(":"))
        total_seconds = hours * 3600 + minutes * 60 + seconds

        # Calcular el total de conteos de emociones
        total_count = sum(self.emotion_counts.values())
        
        # Calcular porcentajes
        percentages = {}
        if total_count == 0:
            percentages = {emotion: 0 for emotion in emotions}
        else:
            percentages = {emotion: (self.emotion_counts[emotion] / total_count) * 100 for emotion in emotions}

        return {
            "duration": total_seconds,  # Agregando duración
            "emotion_counts": dict(self.emotion_counts),  # Conteos de emociones
            "percentages": percentages  # Porcentajes calculados
        }




    def on_selection(self, selection):
        x1, y1, x2, y2 = map(int, selection)
        self.capture_coords = (min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        self.start_analysis()

    def update_elapsed_time(self):
        if self.running:
            current_time = datetime.datetime.now()
            elapsed_time = current_time - self.start_time
            hours, remainder = divmod(elapsed_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.elapsed_time_var.set(f"{hours:02}:{minutes:02}:{seconds:02}")
            self.after(1000, self.update_elapsed_time)  # Actualiza cada segundo

    def process_frame(self):
        if not self.running or self.capture_coords is None:
            return

        x, y, w, h = self.capture_coords
        mp_face_mesh = mp.solutions.face_mesh
        if not hasattr(self, 'face_mesh'):
            self.face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        mp_drawing = mp.solutions.drawing_utils

        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            img = np.array(screenshot)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            results = self.face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    for landmark in face_landmarks.landmark:
                        x_pos = int(landmark.x * img.shape[1])
                        y_pos = int(landmark.y * img.shape[0])
                        cv2.circle(img_rgb, (x_pos, y_pos), 1, (0, 255, 0), -1)

                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                img_resized = cv2.resize(img_gray, (48, 48))
                img_array = np.expand_dims(img_resized, axis=-1)  # Añadir canal de color único
                img_array = np.expand_dims(img_array, axis=0)
                img_array = img_array / 255.0

                predictions = model.predict(img_array)
                emotion_index = np.argmax(predictions)
                emotion = emotions[emotion_index]
                self.emotion_counts[emotion] += 1  # Incrementa el conteo de la emoción detectada

                # Agregar emoción al historial
                self.history.append(emotion)

                # Actualizar la etiqueta de emoción
                self.emotion_label.config(text=f'Emoción detectada: {emotion}')

            else:
                self.emotion_label.config(text='Rostro no detectado')

            img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            imgtk = ImageTk.PhotoImage(image=img_pil)
            self.vid_label.imgtk = imgtk
            self.vid_label.configure(image=imgtk)
        except Exception as e:
            print(f"Error al capturar el marco: {e}")

        if self.running:
            self.after(50, self.process_frame)

    def go_back(self):
        self.master.show_user_view_screen(self.user_data)

    def on_close(self):
        if messagebox.askokcancel("Cerrar", "¿Estás seguro de que deseas cerrar la aplicación?"):
            self.stop_analysis()
            plt.close('all')  # Cerrar cualquier ventana o gráfico activo de Matplotlib

            # Limpiar la sesión de TensorFlow si es necesario
            tf.keras.backend.clear_session()
            self.master.destroy()  # Cerrar la ventana principal
            self.master.quit()  # Salir del mainloop() para finalizar la ejecución correctamente