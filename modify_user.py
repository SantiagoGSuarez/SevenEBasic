import tkinter as tk
import customtkinter as ctk  
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import io
from database import create_connection
from tkcalendar import DateEntry
from datetime import datetime
import cv2
import re  




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

class ModifyUserScreen(tk.Frame):
    def __init__(self, master, user_data):
        super().__init__(master, bg=IFSUL_WHITE)
        self.master = master
        self.user_data = user_data

        self.photo_data = None  # Inicializar photo_data para almacenar la imagen
        
        self.validate_alpha_input = master.register(self.validate_alpha_input)


        self.create_widgets()

        # Vincular el evento de cierre de la ventana principal al método on_close
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def validate_date_input(self, char):
        """Valida la entrada en el campo de fecha para permitir solo números y guiones."""
        return char.isdigit() or char in ("-", "")  # Permitir dígitos y guiones

    def is_valid_date(self,date_str):
        """Verifica si la fecha está en el formato 'YYYY-MM-DD'."""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')  # Cambia a '%d-%m-%Y' si usas ese formato
            return True
        except ValueError:
            return False


    def load_activities(self, admin_id):
        conn = create_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT idActividad, nombre FROM actividad WHERE idAdmin = %s", (admin_id,))
            activities = cursor.fetchall()
        return activities
    
    def create_widgets(self):
        # Banner Gris
        banner_frame = tk.Frame(self, bg=IFSUL_DARK_GREY, height=100, pady=10, padx=35)
        banner_frame.pack(fill="x")

        # Frame para la etiqueta del nombre del administrador, alineada a la derecha
        admin_frame = tk.Frame(banner_frame, bg=IFSUL_DARK_GREY)
        admin_frame.pack(side="top", anchor="ne", padx=10, pady=5)

        # Etiqueta del nombre del administrador
        admin_label = tk.Label(admin_frame, text=f"Administrador: {self.master.admin_name}", bg=IFSUL_DARK_GREY, fg=IFSUL_WHITE, font=("Helvetica", 15, "bold"))
        admin_label.pack()

        # Frame para los botones en el banner
        button_frame = tk.Frame(banner_frame, bg=IFSUL_DARK_GREY)
        button_frame.pack(side="bottom", fill="x")

        # Cargar la imagen para el botón de "Retroceder"
        izquierda_image = ctk.CTkImage(Image.open("Resources/izquierda3.png"), size=(35, 35))

        # Botón de "Retroceder"
        ctk.CTkButton(button_frame, text="",image=izquierda_image, command=self.master.show_main_screen, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER,  width=10, height=40, corner_radius=10).pack(side="left", padx=10)

        # Título de la sección de modificación de usuarios
        tk.Label(self, text="Editar Usuario:", bg=IFSUL_WHITE, fg=IFSUL_GREEN, font=("Helvetica", 20, "bold")).pack(side="top", anchor="w", padx=50, pady=30)

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

        # Cargar imagen actual o por defecto
        if self.user_data.get('foto'):
            image = Image.open(io.BytesIO(self.user_data['foto']))
        else:
            image = Image.open("Resources/DefaultUser.png")

        image = image.resize((150, 150), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        self.photo_label.config(image=self.photo)

        # Campo de foto y botón de selección en el marco de imagen
        self.photo_path = tk.StringVar(value="")  # Iniciar vacío
        self.photo_entry = ctk.CTkEntry(image_frame, textvariable=self.photo_path, font=FONT_LARGE, width=200, fg_color=IFSUL_GREY, text_color=IFSUL_BLACK, border_color="lightgrey",border_width=2, state="readonly")
        self.photo_entry.pack(pady=5)

        ctk.CTkButton(image_frame, text="Seleccionar Foto", command=self.select_image, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=200, height=30, corner_radius=10).pack(pady=5)

        # Botón "Tomar Foto" colocado justo debajo de "Seleccionar Foto"
        ctk.CTkButton(image_frame, text="Tomar Foto", command=self.open_camera_window, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=200, height=30, corner_radius=10).pack(pady=5)


        # Usar pack para las etiquetas y los campos en el marco de datos
        self.entries = []
        self.fields = [
            ("Nombre:", ctk.CTkEntry(data_frame, font=FONT_LARGE,fg_color=IFSUL_WHITE, text_color=IFSUL_BLACK, border_color="lightgrey",border_width=2,validate="key",validatecommand=(self.validate_alpha_input, '%S'))),
            ("Apellido:", ctk.CTkEntry(data_frame, font=FONT_LARGE,fg_color=IFSUL_WHITE, text_color=IFSUL_BLACK, border_color="lightgrey",border_width=2,validate="key",validatecommand=(self.validate_alpha_input, '%S'))),
            ("Fecha de Nacimiento:", DateEntry(data_frame, font=FONT_MEDIUM, date_pattern='y-mm-dd')),  # Usa un DateEntry para la fecha
            ("Email:", ctk.CTkEntry(data_frame, font=FONT_LARGE,fg_color=IFSUL_WHITE, text_color=IFSUL_BLACK, border_color="lightgrey",border_width=2)),
        ]

        for i, (field, widget) in enumerate(self.fields):
            label = tk.Label(data_frame, text=field, fg=IFSUL_GREEN, font=FONT_LARGE, anchor="w", bg=IFSUL_GREY)
            label.pack(anchor="w", padx=10, pady=5)
            if widget:
                widget.pack(fill="x", padx=10, pady=5)
                self.entries.append(widget)

        self.fields[2][1].bind("<KeyRelease>", self.on_date_entry_change)  # Bind the KeyRelease event


        # Cargar actividades desde la base de datos
        self.activities = self.load_activities(self.master.current_admin_id)

        # Crear un diccionario para mapear id de actividad a nombre
        self.activities_dict = {activity[0]: activity[1] for activity in self.activities}

        # Obtener el ID de actividad del usuario
        user_activity_id = self.user_data.get('idactividad')


        # Recuperar el nombre de la actividad correspondiente usando el ID
        user_activity_name = self.activities_dict.get(user_activity_id, "--Seleccionar una opción--")

        # Inicializar selected_activity con el nombre de la actividad correspondiente
        self.selected_activity = tk.StringVar(value=user_activity_name)

        # Crear la etiqueta para seleccionar la actividad
        activity_label = tk.Label(data_frame, text="Actividad:", fg=IFSUL_GREEN, font=FONT_LARGE, anchor="w", bg=IFSUL_GREY)
        activity_label.pack(anchor="w", padx=10, pady=5)  # Etiqueta de Actividad

        # Verificar si hay actividades disponibles
        if self.activities:  # Hay actividades
            # Crear una lista con los nombres de las actividades
            activity_menu_options = [activity[1] for activity in self.activities]  # solo nombres
            
            # Crear el OptionMenu para seleccionar actividad
            self.activity_menu = tk.OptionMenu(data_frame, self.selected_activity, *activity_menu_options)
            self.activity_menu.config(width=15)  # Ajustar el ancho del menú
            self.activity_menu.pack(fill="x",padx=10, pady=5)
        else:
            # Si no hay actividades, mostrar un mensaje
            tk.Label(data_frame, text="No hay actividades registradas", bg=IFSUL_GREY).pack(anchor="w", padx=10, pady=5)


       




        # Configurar los radiobuttons para Género
        gender_label = tk.Label(data_frame, text="Género:", fg=IFSUL_GREEN, font=FONT_LARGE, anchor="w", bg=IFSUL_GREY)
        gender_label.pack(anchor="w", padx=10, pady=5)

        gender_frame = tk.Frame(data_frame, bg=IFSUL_GREY)
        gender_frame.pack(fill="x", padx=10, pady=5)
        self.selected_gender = tk.StringVar()
        self.selected_gender.set(self.user_data.get('genero', ''))
        ctk.CTkRadioButton(gender_frame, text="Femenino", variable=self.selected_gender, value="Femenino", text_color=IFSUL_GREEN, font=FONT_LARGE, fg_color=IFSUL_LIGHT_GREEN, hover_color=IFSUL_HOVER).pack(side="left", padx=5)
        ctk.CTkRadioButton(gender_frame, text="Masculino", variable=self.selected_gender, value="Masculino", text_color=IFSUL_GREEN, font=FONT_LARGE, fg_color=IFSUL_LIGHT_GREEN, hover_color=IFSUL_HOVER).pack(side="left", padx=5)

        # Inicializar los campos con los datos del usuario
        self.entries[0].insert(0, self.user_data.get('nome', ''))
        self.entries[1].insert(0, self.user_data.get('sobrenome', ''))
        fecha_nacimiento = self.user_data.get('fecha')
        if fecha_nacimiento:
            self.entries[2].set_date(fecha_nacimiento)
        self.entries[3].insert(0, self.user_data.get('email', ''))

        # Frame para el botón de guardar
        buttons_frame = tk.Frame(image_frame)
        buttons_frame.pack(fill="x", side="bottom")

        ctk.CTkButton(buttons_frame, text="Guardar cambios", command=self.on_save, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=150, height=40, corner_radius=10).pack(side="bottom", padx=10, pady=5)

    def on_date_entry_change(self, event):
        """Limita la entrada a números y guiones."""
        value = self.entries[2].get()  # Obtener el valor actual del DateEntry
        
        # Patrón para el formato de fecha (YYYY-MM-DD)
        pattern = r"^\d{4}-\d{2}-\d{2}$"

        # Filtrar el valor y mantener solo los caracteres válidos
        filtered_value = ''.join(c for c in value if c.isdigit() or c == '-')
        # Actualizar el campo solo si el valor ha cambiado
        if value != filtered_value:
            self.entries[2].delete(0, tk.END)  # Limpiar el campo
            self.entries[2].insert(0, filtered_value)  # Insertar el valor filtrado
    
    def validate_alpha_input(self, char):
        # Verifica si el carácter es una letra (mayúscula o minúscula)
        return bool(re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ ]*$', char))

    def load_user_photo(self):
        # Aquí puedes cargar la foto del usuario existente y mostrarla
        if self.user_data and 'foto' in self.user_data:
            self.photo_data = self.user_data['foto']
            image = Image.open(io.BytesIO(self.photo_data))  # Cargar imagen desde datos binarios
            image = image.resize((150, 150), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            self.photo_label.config(image=self.photo)

    def select_image(self):
        file_path = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            self.photo_path.set(file_path)
            image = Image.open(file_path)
            image = image.resize((150, 150), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            self.photo_label.config(image=self.photo)

            with open(file_path, "rb") as file:
                self.photo_data = file.read()  # Guardar los datos de la imagen

    def open_camera_window(self):
        self.camera_window = tk.Toplevel(self.master)
        self.camera_window.title("Tomar Foto")
        self.camera_window.geometry("800x600")
        self.camera_window.iconbitmap("Resources/icono4.ico")  # Agregar ícono a la ventana

        # Centrar la ventana
        self.center_window(self.camera_window, 800, 600)

        # Crear el label para la cámara (inicialmente oculto)
        self.camera_error_label = tk.Label(self.camera_window, text="Cámara no disponible, verifique la conexión de la cámara.", fg="red", bg=IFSUL_GREY, font=("Helvetica", 12, "bold"))
        
        # Intentar abrir la cámara
        self.video_capture = cv2.VideoCapture(0)
        
        if not self.video_capture.isOpened():  # Verificar si la cámara no se abrió correctamente
            self.camera_error_label.pack(pady=10)  # Mostrar el mensaje de error
            self.video_label = None  # No crear el label de video
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

    def read_image(self, file_path):
        with open(file_path, 'rb') as file:
            return file.read()
    
    
    def on_save(self):
        name = self.entries[0].get()
        surname = self.entries[1].get()
        date = self.entries[2].get()
        email = self.entries[3].get()
        activity = self.selected_activity.get()
        gender = self.selected_gender.get()


        # Validar formato de fecha
        if not self.is_valid_date(date):
            messagebox.showerror("Error", "El formato de fecha no es válido. Debe ser YYYY-MM-DD.")
            return


        # Validar email antes de continuar
        if not is_valid_email(email):
            messagebox.showerror("Error", "El formato del email no es válido.")
            return

        # Obtener el idActividad correspondiente al nombre seleccionado
        activity_id = [key for key, value in self.activities_dict.items() if value == activity]

        if not activity_id:
            messagebox.showwarning("Advertencia", "Actividad no válida seleccionada.")
            return
        activity_id = activity_id[0]  # Tomar el primer (y único) idActividad encontrado

        if not (name and surname and date and email and activity and gender):
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos")
            return

        # Usar self.photo_data directamente en lugar de leer de photo_path
        if self.photo_data is not None:  # Si hay una foto tomada o seleccionada
            photo_data = self.photo_data
        else:  # Mantener la foto existente
            photo_data = self.user_data.get('foto')

        conn = create_connection()
        cursor = conn.cursor()
        try:
            query = """
            UPDATE usuario
            SET nome = %s, sobrenome = %s, fecha = %s, email = %s, genero = %s, idActividad = %s, foto = %s
            WHERE idusuario = %s
            """
            cursor.execute(query, (name, surname, date, email, gender, activity_id, photo_data, self.user_data.get('idusuario')))
            conn.commit()

            messagebox.showinfo("Éxito", "Usuario modificado exitosamente")
            self.master.show_main_screen()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Error al modificar el usuario: {e}")
        finally:
            conn.close()

    def on_close(self):  # Agregado para manejar el cierre de la ventana
        if messagebox.askokcancel("Cerrar", "¿Estás seguro de que deseas cerrar la aplicación?"):
            self.master.destroy()  # Cerrar la ventana principal