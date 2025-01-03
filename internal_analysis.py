import tkinter as tk
import customtkinter as ctk  
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp
from collections import deque
import datetime
from database import create_connection
from collections import defaultdict



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

class InternalAnalysisScreen(tk.Frame):
    def __init__(self, master, user_data):
        super().__init__(master, bg=IFSUL_WHITE)
        self.is_retrocediendo = False  # Inicializa el flag

        self.master = master
        self.user_data = user_data

        # Inicializa MediaPipe FaceMesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )




        self.cap = None
        self.running = False
        self.history = deque(maxlen=10)  # Historial de predicciones para suavizado
        self.emotion_counts = defaultdict(int)  # Inicializa el conteo de emociones

        # Tiempo
        self.start_time = None  # Para el conteo de tiempo
        self.elapsed_time_var = tk.StringVar(value="00:00:00")  # Variable para el tiempo transcurrido

        self.create_widgets()
        # Vincular el evento de cierre de la ventana al método on_close
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

        ctk.CTkButton(top_banner_frame, text="", image=izquierda_image, command=self.go_back, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=10, height=40,corner_radius=10).pack(side="left", padx=10)

        # Frame para la cámara
        self.video_frame = tk.Frame(self, bg=IFSUL_WHITE)
        self.video_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Label para mostrar la imagen de la cámara
        self.vid_label = tk.Label(self.video_frame)
        self.vid_label.pack(fill="both", expand=True)

        # Label para el mensaje de error y la emoción detectada
        self.error_label = tk.Label(self.video_frame, text="", fg="red", bg=IFSUL_WHITE, font=FONT_MEDIUM)
        self.error_label.pack(pady=(10, 0))

        banner_frame = tk.Frame(self, bg=IFSUL_DARK_GREY, height=100, pady=10, padx=35)
        banner_frame.pack(side="bottom", fill="x")

        button_frame = tk.Frame(banner_frame, bg=IFSUL_DARK_GREY)
        button_frame.pack(pady=20)

        # Cargar la imagen para el botón de "Retroceder"
        play_image = ctk.CTkImage(Image.open("Resources/play.png"), size=(35, 35))
        # Cargar la imagen para el botón de "Retroceder"
        detener_image = ctk.CTkImage(Image.open("Resources/detener.png"), size=(35, 35))


        # Botones "Iniciar" y "Detener"
        start_button = ctk.CTkButton(button_frame, text="",image=play_image, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=120, height=40, command=self.start_analysis)
        stop_button = ctk.CTkButton(button_frame, text="",image=detener_image, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=120, height=40, command=self.stop_camera)

        start_button.pack(side="left", padx=(0, 20))
        stop_button.pack(side="left", padx=(20, 0))

        # Label para mostrar el tiempo transcurrido
        self.elapsed_time_label = tk.Label(self.video_frame, textvariable=self.elapsed_time_var, bg=IFSUL_WHITE, font=FONT_MEDIUM)
        self.elapsed_time_label.pack(pady=(10, 0))

    def start_analysis(self):
        self.start_time = datetime.datetime.now()  # Guarda el tiempo de inicio
        self.running = True  # Asegúrate de que esté en True
        self.update_elapsed_time()  # Comienza el conteo del tiempo
        self.start_camera()  # Inicia la cámara

    def update_elapsed_time(self):
        if self.running:
            current_time = datetime.datetime.now()
            elapsed_time = current_time - self.start_time
            hours, remainder = divmod(elapsed_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.elapsed_time_var.set(f"{hours:02}:{minutes:02}:{seconds:02}")
            self.after(1000, self.update_elapsed_time)  # Actualiza cada segundo
    
    def start_camera(self):
        if self.cap is not None:
            self.stop_camera()

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.error_label.config(text="Error: Conecte la cámara y vuelva a intentarlo de nuevo")
            print("No se puede acceder a la cámara.")
            return

        self.error_label.config(text="")  # Limpiar el mensaje de error
        self.update_camera()  # Mueve la llamada aquí

    def stop_camera(self):
        self.running = False
        if self.cap is not None:
            if self.cap.isOpened():
                self.cap.release()
            self.cap = None
        self.error_label.config(text="La cámara ha sido detenida.")
        self.vid_label.config(image=None)  # Limpiar la imagen de la cámara
        self.vid_label.image = None  # Asegurarse de liberar la referencia a la imagen
        
        # Solo guardar resultados y mostrar la pantalla si no se está cerrando la aplicación
        if not self.is_retrocediendo:
            results = self.calculate_percentages()

            # Añadimos el tiempo en formato correcto a los resultados
            results['formatted_time'] = self.elapsed_time_var.get()
            results['start_time'] = self.start_time  # Agregamos el start_time a los resultados


            self.master.show_results_screen(self.user_data, results)
        
        tf.keras.backend.clear_session()  # Limpiar la sesión de TensorFlow si es necesario
        
       
        # Reinicia el flag
        self.is_retrocediendo = False  # Reinicia el flag al detener
        # Reinicia el tiempo
        self.start_time = None  # Reinicia el tiempo al detener
        self.elapsed_time_var.set("00:00:00")  # Resetea el contador visual
    
    def calculate_percentages(self):
        # Calcular la duración total
        duration = self.elapsed_time_var.get()
        # Convertir duración a segundos
        hours, minutes, seconds = map(int, duration.split(":"))
        total_seconds = hours * 3600 + minutes * 60 + seconds

        # Calcular porcentajes
        total_count = sum(self.emotion_counts.values())
        if total_count == 0:
            percentages = {emotion: 0 for emotion in emotions}
        else:
            percentages = {emotion: (self.emotion_counts[emotion] / total_count) * 100 for emotion in emotions}
        return {
            "duration": total_seconds,
            "percentages": percentages
        }
        

    def update_camera(self):
        if self.running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (600, 400))  # Ajusta el tamaño aquí
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.mp_face_mesh.process(frame_rgb)

                # Inicializa la emoción detectada como "No detectado"
                smoothed_emotion = "No detectado"

                # Dibuja los puntos faciales y procesa la emoción
                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:
                        points = [(int(point.x * frame.shape[1]), int(point.y * frame.shape[0])) for point in face_landmarks.landmark]

                        # Dibuja los puntos de la malla facial
                        for point in points:
                            cv2.circle(frame, point, 1, (0, 255, 0), -1)

                    # Define la región de interés (ROI) usando los puntos de la malla facial
                    x_min = min([p[0] for p in points])
                    x_max = max([p[0] for p in points])
                    y_min = min([p[1] for p in points])
                    y_max = max([p[1] for p in points])

                    if x_min < 0 or y_min < 0 or x_max > frame.shape[1] or y_max > frame.shape[0]:
                        x_min = 0
                        y_min = 0
                        x_max = frame.shape[1]
                        y_max = frame.shape[0]

                    face = frame[y_min:y_max, x_min:x_max]

                    if face.size == 0:
                        self.error_label.config(text="Error: La región de interés está vacía.")
                        return

                    # Preprocesa la imagen para la predicción
                    face = cv2.resize(face, (48, 48))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)  # Convierte a escala de grises
                    face = np.expand_dims(face, axis=-1)  # Añade un canal para la imagen en escala de grises
                    face = face / 255.0
                    face = np.reshape(face, (1, 48, 48, 1))

                    # Realiza la predicción
                    prediction = model.predict(face)  # Asegúrate de usar la imagen procesada correctamente
                    emotion_label = np.argmax(prediction)
                    smoothed_emotion = emotions[emotion_label]

                    # Añadir la emoción actual al historial
                    self.history.append(smoothed_emotion)
                    smoothed_emotion = max(set(self.history), key=self.history.count)
                    
                    # Almacena la emoción detectada en el historial y actualiza el conteo
                    self.emotion_counts[smoothed_emotion] += 1  # Incrementa el conteo de la emoción actual

                else:
                    # No se detecta rostro
                    smoothed_emotion = "Rostro no detectado"

                # Actualizar la etiqueta de emoción
                self.error_label.config(text=f"Emoción detectada: {smoothed_emotion}")


                self.vid_label.image = None  # Limpiar la referencia a la imagen anterior


                # Mostrar la imagen en el widget Tkinter
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                self.vid_label.config(image=imgtk)
                self.vid_label.image = imgtk

            else:
                self.error_label.config(text="Error: No se pudo acceder a la cámara. Verifique la conexión.")
                self.stop_camera()

            # Continúa el loop si running es True
            if self.running:
                self.after(10, self.update_camera)
        else:
            self.error_label.config(text="Error: La cámara no está abierta o no está en ejecución.")

    def go_back(self):
        self.is_retrocediendo = True  # Indica que se está retrocediendo
        self.stop_camera()
        self.master.show_user_view_screen(self.user_data)  # Asumiendo que tienes esta función en la clase principal

    def on_close(self):
        # Muestra un mensaje de confirmación antes de cerrar la ventana
        if messagebox.askokcancel("Cerrar", "¿Estás seguro de que deseas cerrar la aplicación?"):
            self.is_retrocediendo = True  # Indica que se está retrocediendo
            self.stop_camera()  # Detener la cámara y liberar recursos
            plt.close('all')  # Cerrar cualquier ventana o gráfico activo de Matplotlib

            # Limpiar la sesión de TensorFlow si es necesario
            tf.keras.backend.clear_session()
            self.master.quit()  # Finaliza el mainloop de Tkinter

            self.master.destroy()  # Cerrar la ventana principal
