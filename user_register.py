import tkinter as tk
import customtkinter as ctk  
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from database import create_connection
from tkcalendar import DateEntry
import mysql.connector
import cv2
import re
from datetime import datetime




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


        
def is_valid_email(email):
        # Expresión regular para validar el formato del email
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None


class UserRegisterScreen(tk.Frame):
    def __init__(self, master, show_main_screen):
        super().__init__(master, bg=IFSUL_WHITE)
        self.master = master
        self.show_main_screen = show_main_screen

        self.validate_alpha_input = master.register(self.validate_alpha_input)


        self.pack(expand=True)
        self.create_widgets()

        # Vincular el evento de cierre de la ventana principal al método on_close
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def is_valid_date(self,date_str):
        """Verifica si la fecha está en el formato 'YYYY-MM-DD'."""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')  # Cambia a '%d-%m-%Y' si usas ese formato
            return True
        except ValueError:
            return False
        
    def validate_date_input(self, char):
        """Valida la entrada en el campo de fecha para permitir solo números y guiones."""
        return char.isdigit() or char in ("-", "")  # Permitir dígitos y guiones


    def create_widgets(self):
        # Banner Verde
        banner_frame = tk.Frame(self, bg=IFSUL_DARK_GREY, height=100, pady=10, padx=35)
        banner_frame.pack(fill="x")

        # Frame para la etiqueta del nombre del administrador, alineada a la derecha
        admin_frame = tk.Frame(banner_frame, bg=IFSUL_DARK_GREY)
        admin_frame.pack(side="top", anchor="ne", padx=10, pady=5)  # Colocado en la parte superior derecha

        # Etiqueta del nombre del administrador
        admin_label = tk.Label(admin_frame, text=f"Administrador: {self.master.admin_name}", bg=IFSUL_DARK_GREY, fg=IFSUL_WHITE, font=("Helvetica", 15, "bold"))
        admin_label.pack()

        # Frame para los botones en el banner
        button_frame = tk.Frame(banner_frame, bg=IFSUL_DARK_GREY)
        button_frame.pack(side="bottom", fill="x")  # Ahora se alinea al fondo del banner


        # Cargar la imagen para el botón de "Retroceder"
        izquierda_image = ctk.CTkImage(Image.open("Resources/izquierda3.png"), size=(35, 35))

        # Botón de "Retroceder"
        ctk.CTkButton(button_frame, text="", image=izquierda_image, command=self.show_main_screen, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=10, height=40, corner_radius=10).pack(side="left", padx=10)

       
        # Título de la sección de registro usuarios
        tk.Label(self, text="Registro de Usuario:", bg=IFSUL_WHITE, fg=IFSUL_GREEN, font=("Helvetica", 20, "bold")).pack(side="top", anchor="w", padx=50, pady=30)

        container = tk.Frame(self, bg=IFSUL_GREY, width=1300)
        container.pack(padx=10, pady=10)


        # Crear un marco para los datos de usuario y otro para la imagen
        data_frame = tk.Frame(container, bg=IFSUL_GREY)
        data_frame.pack(side="left", fill="y", padx=10, pady=10)

        image_frame = tk.Frame(container, bg=IFSUL_GREY)
        image_frame.pack(side="right", fill="y", padx=10, pady=10)

        # Visualizador de foto
        self.photo_label = tk.Label(image_frame, bg=IFSUL_GREY)
        self.photo_label.pack(pady=10)

        # Cargar imagen por defecto
        self.default_image = Image.open("Resources/DefaultUser.png")
        self.default_image = self.default_image.resize((150, 150), Image.Resampling.LANCZOS)
        self.default_photo = ImageTk.PhotoImage(self.default_image)
        self.photo_label.config(image=self.default_photo)

        # Campo de foto y botón de selección en el marco de imagen
        self.photo_path = tk.StringVar()
        self.photo_entry = ctk.CTkEntry(image_frame, textvariable=self.photo_path, font=FONT_LARGE, width=200, fg_color=IFSUL_GREY, text_color=IFSUL_BLACK, border_color="lightgrey",border_width=2, state="readonly")
        self.photo_entry.pack(pady=5)

        ctk.CTkButton(image_frame, text="Seleccionar Foto", command=self.select_image, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=200, height=30, corner_radius=10).pack(pady=5)


        # Botón "Tomar Foto"
        ctk.CTkButton(image_frame, text="Tomar Foto", command=self.open_camera_window, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=200, height=30, corner_radius=10).pack(pady=5)
        
        # Usar pack para las etiquetas y los campos en el marco de datos
        self.entries = []
        self.fields = [
            ("Nombre:", ctk.CTkEntry(data_frame, font=FONT_LARGE,fg_color=IFSUL_WHITE, text_color=IFSUL_BLACK, border_color="lightgrey",border_width=2,validate="key",validatecommand=(self.validate_alpha_input, '%S'))),
            ("Apellido:", ctk.CTkEntry(data_frame, font=FONT_LARGE,fg_color=IFSUL_WHITE, text_color=IFSUL_BLACK, border_color="lightgrey",border_width=2,validate="key",validatecommand=(self.validate_alpha_input, '%S'))),
            ("Fecha de Nacimiento:", DateEntry(data_frame, font=FONT_MEDIUM, date_pattern='y-mm-dd')),
            ("Email:", ctk.CTkEntry(data_frame, font=FONT_LARGE,fg_color=IFSUL_WHITE, text_color=IFSUL_BLACK, border_color="lightgrey",border_width=2)),
        ]

        for field, widget in self.fields:
            label = tk.Label(data_frame, text=field, fg=IFSUL_GREEN, font=FONT_LARGE, anchor="w", bg=IFSUL_GREY)
            label.pack(anchor="w", padx=10, pady=5)
            if widget:
                widget.pack(fill="x", padx=10, pady=5)
                self.entries.append(widget)

        self.fields[2][1].bind("<KeyRelease>", self.on_date_entry_change)  # Bind the KeyRelease event


        # Cargar actividades desde la base de datos
        self.activities = self.load_activities()
        self.activities.insert(0, "--Seleccionar una opción--")  # Agregar la opción predeterminada
        self.selected_activity = tk.StringVar(value=self.activities[0])  # Valor por defecto

        # Crear el OptionMenu para seleccionar la actividad
        activity_label = tk.Label(data_frame, text="Actividad:", fg=IFSUL_GREEN, font=FONT_LARGE, anchor="w", bg=IFSUL_GREY)
        activity_label.pack(anchor="w", padx=10, pady=5)  # Etiqueta de Actividad

       # Verificar si hay actividades disponibles
        if len(self.activities) > 1:  # Hay más de solo la opción por defecto
            # Crear una lista para el OptionMenu sin la opción "Seleccionar actividad"
            activity_menu_options = self.activities[1:]  # Excluir la primera opción

            activity_menu = tk.OptionMenu(data_frame, self.selected_activity, *activity_menu_options)
            activity_menu.pack(fill="x", padx=10, pady=5)  # Coloca el OptionMenu debajo de la etiqueta
        else:
            # Si no hay actividades, mostrar un mensaje
            tk.Label(data_frame, text="No hay actividades registradas", bg=IFSUL_GREY).pack(anchor="w", padx=10, pady=5)
                
        # Crear el marco para los radiobuttons de género
        gender_label = tk.Label(data_frame, text="Género:", fg=IFSUL_GREEN, font=FONT_LARGE, anchor="w", bg=IFSUL_GREY)
        gender_label.pack(anchor="w", padx=10, pady=5)  # Etiqueta de Género

        gender_frame = tk.Frame(data_frame, bg=IFSUL_GREY)
        gender_frame.pack(fill="x", padx=10, pady=5)
        self.selected_gender = tk.StringVar()
        self.selected_gender.set(None)

        # Configurar los radiobuttons para Género
        ctk.CTkRadioButton(gender_frame, text="Femenino", variable=self.selected_gender, value="Femenino", text_color=IFSUL_GREEN, font=FONT_LARGE, fg_color=IFSUL_LIGHT_GREEN, hover_color=IFSUL_HOVER).pack(side="left", padx=5)
        ctk.CTkRadioButton(gender_frame, text="Masculino", variable=self.selected_gender, value="Masculino", text_color=IFSUL_GREEN, font=FONT_LARGE, fg_color=IFSUL_LIGHT_GREEN, hover_color=IFSUL_HOVER).pack(side="left", padx=5)

        # Frame para el botón de registrar, ubicado en la parte inferior derecha
        buttons_frame = tk.Frame(container, bg=IFSUL_WHITE)
        buttons_frame.pack(pady=20, fill="x", side="bottom")

        ctk.CTkButton(image_frame, text="Registrar", command=self.on_register, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=150, height=40, corner_radius=10).pack(side="bottom", padx=10, pady=5)
    
    def on_date_entry_change(self, event):
        """Limita la entrada a números y guiones."""
        # Obtener el valor actual del DateEntry
        value = self.entries[2].get()

        # Patrón para formato de fecha (YYYY-MM-DD)
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        
        # Permitir borrado o edición sin reinserción mientras se escribe
        if not re.match(pattern, value) and value:
            # Limitar el valor a caracteres válidos (dígitos y guiones)
            filtered_value = ''.join(c for c in value if c.isdigit() or c == '-')
            
            # Actualizar solo si cambia el valor
            if value != filtered_value:
                self.entries[2].delete(0, tk.END)  # Limpiar el campo
                self.entries[2].insert(0, filtered_value)  # Insertar el valor filtrado


    def validate_alpha_input(self, char):
        # Verifica si el carácter es una letra (mayúscula o minúscula)
        return bool(re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ ]*$', char))
    
    def load_activities(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre FROM actividad WHERE idAdmin = %s", (self.master.current_admin_id,))
        activities = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return activities

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((150, 150), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            self.photo_label.config(image=self.photo)
            self.photo_path.set(file_path)  # Actualizar el campo con la dirección del archivo
            
            # Guardar la imagen seleccionada en formato binario
            with open(file_path, 'rb') as file:
                self.photo_data = file.read()  # Guardar la imagen en la variable photo_data

    def read_image(self, file_path):
        with open(file_path, 'rb') as file:
            return file.read()

    def open_camera_window(self):
        self.camera_window = tk.Toplevel(self.master)
        self.camera_window.title("Tomar Foto")
        self.camera_window.geometry("800x600")
        self.camera_window.iconbitmap("Resources/icono4.ico")  # Agregar ícono a la ventana

        # Centrar la ventana
        self.center_window(self.camera_window, 800, 600)

        # Crear el label para la cámara
        self.camera_error_label = tk.Label(self.camera_window, text="Cámara no disponible, verifique la conexión de la cámara.", fg="red", bg=IFSUL_GREY, font=("Helvetica", 12, "bold"))
        self.camera_error_label.pack(pady=10)
        
        # Intentar abrir la cámara
        self.video_capture = cv2.VideoCapture(0)
        
        # Verificar si la cámara se abrió correctamente
        if not self.video_capture.isOpened():
            self.camera_error_label.pack()  # Mostrar el mensaje de error si la cámara no está disponible
        else:
            # Si la cámara está disponible, ocultar el mensaje de error
            self.camera_error_label.pack_forget()
            self.video_label = tk.Label(self.camera_window)
            self.video_label.pack(pady=10)

            # Crear el botón de tomar foto
            ctk.CTkButton(self.camera_window, text="Tomar Foto", command=self.take_photo, font=FONT_LARGE, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, hover_color=IFSUL_HOVER, width=80, height=40, corner_radius=10).pack(pady=10)

            # Iniciar la actualización de la cámara
            self.update_camera()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def update_camera(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir a RGB
            frame = Image.fromarray(frame)
            frame = frame.resize((640, 480), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(frame)
            self.video_label.config(image=self.photo)
        self.video_label.after(10, self.update_camera)

    def take_photo(self):
        ret, frame = self.video_capture.read()  # Lee el frame antes de liberar la captura
        if ret:
            # Convertir el frame a formato RGB y luego a una imagen de PIL
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Cambiar el formato a RGB
            image = Image.fromarray(frame)  # Crear una imagen de PIL desde el frame
            image = image.resize((150, 150), Image.Resampling.LANCZOS)  # Redimensionar la imagen
            self.photo = ImageTk.PhotoImage(image)  # Crear un objeto PhotoImage
            self.photo_label.config(image=self.photo)  # Actualizar la etiqueta de la imagen

            # Almacena la imagen en formato binario en una variable
            from io import BytesIO
            buffer = BytesIO()
            image.save(buffer, format="PNG")  # Guardar en un buffer en formato PNG
            self.photo_data = buffer.getvalue()  # Obtener los datos de la imagen en binario

        self.video_capture.release()  # Asegúrate de liberar el recurso de la cámara
        self.camera_window.destroy()  # Cierra la ventana de la cámara

    def update_photo_display(self, filename):
        image = Image.open(filename)
        image = image.resize((150, 150), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        self.photo_label.config(image=self.photo)


    def on_register(self):

        # Verificar que se haya seleccionado una actividad válida
        if self.selected_activity.get() == "--Seleccionar una opción--":
            messagebox.showwarning("Advertencia", "Debe seleccionar una actividad antes de registrar el usuario.")
            return  # Detener el registro si no se ha seleccionado una actividad válida


        # Acceder a las entradas a través de self.entries
        name = self.entries[0].get()
        surname = self.entries[1].get()
        date = self.entries[2].get()  # Nueva fecha de nacimiento
        email = self.entries[3].get()
        gender = self.selected_gender.get()
        activity = self.selected_activity.get()

        # Validar formato de fecha
        if not self.is_valid_date(date):
            messagebox.showerror("Error", "El formato de fecha no es válido. Debe ser YYYY-MM-DD.")
            return

        # Verificar si la actividad es la opción predeterminada
        if activity == "Seleccionar actividad":
            messagebox.showwarning("Advertencia", "Debes seleccionar una actividad.")
            return

        if not (name and surname and date and email and activity and gender):
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos")
            return
        
        # Validar email antes de continuar
        if not is_valid_email(email):
            messagebox.showerror("Error", "El formato del email no es válido.")
            return

        # Usar la imagen por defecto si no se ha tomado ninguna foto
        if not hasattr(self, 'photo_data'):  # Verifica si photo_data fue definido
            photo_data = self.read_image("Resources/DefaultUser.png")  # Cargar imagen por defecto
        else:
            photo_data = self.photo_data  # Usa la imagen seleccionada o capturada

        conn = create_connection()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO usuario (nome, sobrenome, fecha, email, genero, foto, idAdmin, idActividad) VALUES (%s, %s, %s, %s, %s, %s, %s, (SELECT idActividad FROM actividad WHERE nombre = %s AND idAdmin = %s LIMIT 1))"
            cursor.execute(query, (name, surname, date, email, gender, photo_data, self.master.current_admin_id, activity, self.master.current_admin_id))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente")
            self.show_main_screen()
        except mysql.connector.Error as err:
            conn.rollback()
            messagebox.showerror("Error", f"Error al registrar el usuario: {err}")
        finally:
            conn.close()

    def on_close(self):  # Agregado para manejar el cierre de la ventana
        if messagebox.askokcancel("Cerrar", "¿Estás seguro de que deseas cerrar la aplicación?"):
            self.master.destroy()  # Cerrar la ventana principal