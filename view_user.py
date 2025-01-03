import tkinter as tk
import customtkinter as ctk  
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import io
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import create_connection
import tensorflow as tf
from datetime import date



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

class ViewUserScreen(tk.Frame):
    def __init__(self, master, user_data, show_internal_analysis_screen, show_external_analysis_screen):
        super().__init__(master, bg=IFSUL_WHITE)
        self.master = master
        self.user_data = user_data
        self.show_internal_analysis_screen = show_internal_analysis_screen
        self.show_external_analysis_screen = show_external_analysis_screen
        self.create_widgets()

        # Vincular el evento de cierre de la ventana principal al método on_close
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def get_activity_name(self, activity_id):
        conn = create_connection()
        cursor = conn.cursor()
        
        try:
            query = "SELECT nombre FROM actividad WHERE idActividad = %s"
            cursor.execute(query, (activity_id,))
            activity_name = cursor.fetchone()
            return activity_name[0] if activity_name else "Actividad no encontrada"
        except Exception as e:
            print(f"Error al obtener el nombre de la actividad: {e}")
            return "Error en la consulta"
        finally:
            conn.close()

    def create_widgets(self):
        # Banner Gris
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
        ctk.CTkButton(button_frame, text="", image=izquierda_image, command=self.master.show_main_screen,fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=10, height=40, corner_radius=10).pack(side="left", padx=10)
        



        # Cargar las imágenes para los botones
        editar_image = ctk.CTkImage(Image.open("Resources/editar.png"), size=(30, 30))
        eliminar_image = ctk.CTkImage(Image.open("Resources/eliminar.png"), size=(30, 30))

        # Botón de "eliminar"
        ctk.CTkButton(button_frame, text="", image=eliminar_image,command=self.confirm_delete, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=60, height=40, corner_radius=10).pack(side="right", padx=10)

        # Botón de "editar"
        ctk.CTkButton(button_frame, text="", image=editar_image,command=self.open_modify_user_screen, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=60, height=40, corner_radius=10).pack(side="right", padx=10)
        
        


         # Frame para mostrar los detalles del usuario
        details_frame = tk.Frame(self, bg=IFSUL_WHITE)
        details_frame.pack(pady=20, padx=20, fill="both", expand=True, anchor="center")

        # Crear un frame para la imagen y los datos
        content_frame = tk.Frame(details_frame, bg=IFSUL_GREY, width=900)
        content_frame.pack(pady=20, padx=20, anchor="center")  # Centrar el content_frame dentro del details_frame

        # Mostrar la foto del usuario
        if self.user_data.get('foto'):
            image = Image.open(io.BytesIO(self.user_data['foto']))
            image.thumbnail((200, 200))  # Ajustar el tamaño de la imagen
            photo = ImageTk.PhotoImage(image)
            photo_label = tk.Label(content_frame, image=photo, bg=IFSUL_GREY)
            photo_label.image = photo  # Mantener una referencia para evitar la recolección de basura
            photo_label.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        # Frame para los datos del usuario
        info_frame = tk.Frame(content_frame, bg=IFSUL_GREY)
        info_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nw")

       
       # Frame para el gráfico
        self.chart_frame = tk.Frame(content_frame, bg=IFSUL_GREY)
        self.chart_frame.grid(row=3, column=0, columnspan=2, pady=1, sticky="n")  # Se coloca debajo en el mismo content_frame

        # Llamar a la función para actualizar y mostrar el gráfico
        self.update_user_chart()

       # Obtener la fecha de nacimiento del user_data
        birth_date_str = self.user_data.get('fecha', None)
        birth_date = None

        

        # Verifica si birth_date_str ya es una fecha
        if isinstance(birth_date_str, date):
            birth_date = birth_date_str  # Ya es un objeto date
        elif isinstance(birth_date_str, str):
            try:
                birth_date = date.strptime(birth_date_str, '%Y-%m-%d').date()  # Convierte el string a una fecha
            except ValueError:
                print(f"Formato de fecha inválido: {birth_date_str}")

        # Calcular la edad
        age = self.calculate_age(birth_date)
        activity_id = self.user_data.get('idactividad')
        activity_name = self.get_activity_name(activity_id)
        # Crear y mostrar los atributos en filas separadas
        labels = [
            ('Nombre', f"{self.user_data.get('nome', 'No disponible')} {self.user_data.get('sobrenome', 'No disponible')}"),
            ('Edad', f"{age} años"),
            ('Género', self.user_data.get('genero', 'No disponible')),
            ('Email', self.user_data.get('email', 'No disponible')),
            ('Actividad', activity_name)
        ]

        # Iterar sobre los atributos y crear las etiquetas
        for row, (label_text, value) in enumerate(labels):
            tk.Label(info_frame, text=f"{label_text}:", bg=IFSUL_GREY, fg=IFSUL_GREEN, font=FONT_MEDIUM, anchor="w").grid(row=row, column=0, sticky="w")
            tk.Label(info_frame, text=value, bg=IFSUL_GREY, fg=IFSUL_GREEN, font=FONT_MEDIUM).grid(row=row, column=1, sticky="w")

        # Botón "Ver Análisis"
        view_analysis_button = ctk.CTkButton(info_frame, text="Ver Análisis",command=lambda: self.master.show_view_results_screen(self.user_data), fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=100, height=30, corner_radius=10)
        view_analysis_button.grid(row=len(labels) + 1, column=0, columnspan=2, pady=20, sticky="w")  # Colocado debajo del último atributo

        # Frame para centrar los botones de análisis
        analysis_button_frame = tk.Frame(content_frame, bg=IFSUL_GREY)
        analysis_button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Botón "Análisis Interno"
        internal_analysis_button = ctk.CTkButton(analysis_button_frame, command=lambda:self.check_and_show_internal_analysis(self.user_data), text="Análisis Interno", fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=130, height=40, corner_radius=10)
        internal_analysis_button.pack(side="left", padx=10)

        # Botón "Análisis Externo"
        external_analysis_button = ctk.CTkButton(analysis_button_frame,command=lambda:self.check_and_show_external_analysis(self.user_data), text="Análisis Externo", fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=130, height=40, corner_radius=10)
        external_analysis_button.pack(side="left", padx=10)

        self.pack(fill="both", expand=True)
    
    
    def check_and_show_internal_analysis(self, user_data):
        """Verifica si el usuario tiene una actividad asignada antes de mostrar el análisis interno."""
        activity_id = self.user_data.get('idactividad')  # Obtener el id de actividad del usuario
        
        if not activity_id:
            # Si el usuario no tiene una actividad asignada, mostrar mensaje de advertencia
            messagebox.showwarning("Actividad no asignada", "Debe asignar una actividad al usuario antes de proceder con el análisis.")
        else:
            # Si el usuario tiene actividad asignada, proceder con el análisis
            self.show_internal_analysis_screen(user_data)

    def check_and_show_external_analysis(self, user_data):
        """Verifica si el usuario tiene una actividad asignada antes de mostrar el análisis externo."""
        activity_id = self.user_data.get('idactividad')  # Obtener el id de actividad del usuario
        
        if not activity_id:
            # Si el usuario no tiene una actividad asignada, mostrar mensaje de advertencia
            messagebox.showwarning("Actividad no asignada", "Debe asignar una actividad al usuario antes de proceder con el análisis.")
        else:
            # Si el usuario tiene actividad asignada, proceder con el análisis
            self.show_external_analysis_screen(user_data)
    
    def calculate_age(self, birth_date):
        """Calcula la edad a partir de la fecha de nacimiento en formato 'YYYY-MM-DD'."""
        if birth_date:
            try:
                today = date.today()  # Obtiene la fecha actual
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                return age
            except Exception as e:
                print(f"Error al calcular la edad: {e}")
                return "Error en el cálculo"
        return "No disponible"

    def confirm_delete(self):
        # Mostrar un mensaje de confirmación
        respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar este usuario?")

        if respuesta:
            # Si el usuario confirma, proceder con la eliminación
            self.delete_user()

    def delete_user(self):
        user_id = self.user_data.get('idusuario')  # Asegúrate de que 'id' está en user_data
        if not user_id:
            messagebox.showerror("Error", "No se puede eliminar el usuario, ID no encontrado.")
            return

        conn = create_connection()
        cursor = conn.cursor()

        try:
            query = "DELETE FROM usuario WHERE idusuario = %s"
            cursor.execute(query, (user_id,))
            conn.commit()

            messagebox.showinfo("Usuario Eliminado", "El usuario ha sido eliminado exitosamente.")
            self.master.show_main_screen()  # Volver a la pantalla principal
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"No se pudo eliminar el usuario: {e}")
        finally:
            conn.close()     

    def open_modify_user_screen(self):
        self.master.show_modify_user_screen(self.user_data)


    def update_user_chart(self):
        # Limpiar gráfico anterior
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Consulta base para obtener las emociones promedio de un usuario específico
        connection = create_connection()
        cursor = connection.cursor()

        # Consulta para obtener el promedio de emociones solo para el usuario actual
        query = """
            SELECT 
                AVG(r.ira) AS avg_ira, 
                AVG(r.disgusto) AS avg_disgusto, 
                AVG(r.miedo) AS avg_miedo, 
                AVG(r.feliz) AS avg_feliz,
                AVG(r.neutral) AS avg_neutral, 
                AVG(r.triste) AS avg_triste, 
                AVG(r.sorpresa) AS avg_sorpresa
            FROM resultado r
            WHERE r.idUsuario = %s
        """
        
        params = [self.user_data.get('idusuario')]  # ID del usuario actual

        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if not result or all(val is None for val in result):
            tk.Label(self.chart_frame, text="No existen datos de análisis para este usuario.", bg=IFSUL_GREY, fg=IFSUL_GREEN, font=FONT_MEDIUM).pack(pady=10)
            return

        # Calcular promedios, reemplazando None por 0
        averages = [val if val is not None else 0 for val in result]
        emotions = ['Ira', 'Disgusto', 'Miedo', 'Feliz', 'Neutral', 'Triste', 'Sorpresa']

        # Colores según las emociones
        colors = ['#FF0000',  # Ira: Rojo
                '#008000',  # Disgusto: Verde
                '#000000',  # Miedo: Negro
                '#FFFF00',  # Feliz: Amarillo
                '#808080',  # Neutral: Gris
                '#0000FF',  # Triste: Azul
                '#FFA500']  # Sorpresa: Naranja

        # Crear gráfico
        fig, ax = plt.subplots(figsize=(6, 3))

        # Cambiar el color de fondo de la figura (todo el área del gráfico)
        fig.patch.set_facecolor(IFSUL_GREY)  # Color claro de fondo para la figura
        
        bars = ax.bar(emotions, averages, color=colors)
        ax.set_title("Promedio de Emociones",fontsize=12)
        ax.set_ylabel("Promedio",fontsize=10)
        # Establecer las posiciones de las barras (xticks) y etiquetas con un tamaño de fuente ajustado
        ax.set_xticks(range(len(emotions)))  # Establecer las posiciones de las etiquetas
        ax.set_xticklabels(emotions, fontsize=10)  # Cambiar el tamaño de la fuente de las etiquetas

        # Modificar el tamaño de la fuente de los números en el eje Y
        ax.tick_params(axis='y', labelsize=10)  # Cambiar tamaño de fuente para los números del eje Y

        # Ajustar el límite superior del eje y
        ax.set_ylim(0, max(averages) + 8)

        # Añadir los porcentajes encima de cada barra
        for bar in bars:
            yval = bar.get_height()
            if yval.is_integer():
                ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{int(yval)}%', ha='center', va='bottom', fontsize=10)
            else:
                ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.3f}%', ha='center', va='bottom', fontsize=10)

        # Ajustar el diseño del gráfico para evitar que se corte
        fig.tight_layout()

        # Mostrar gráfico en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Cerrar la figura después de mostrarla
        plt.close(fig)



    def on_close(self):  # Agregado para manejar el cierre de la ventana
        if messagebox.askokcancel("Cerrar", "¿Estás seguro de que deseas cerrar la aplicación?"):
            plt.close('all')  # Cerrar cualquier ventana o gráfico activo de Matplotlib
            # Limpiar la sesión de TensorFlow si es necesario
            tf.keras.backend.clear_session()
            self.master.destroy()  # Cerrar la ventana principal
            self.master.quit()  # Salir del mainloop() para finalizar la ejecución correctamente