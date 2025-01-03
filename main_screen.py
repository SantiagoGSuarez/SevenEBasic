import tkinter as tk
import customtkinter as ctk  
from PIL import Image, ImageTk
import io
from tkinter import messagebox
from database import create_connection
import tensorflow as tf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
import numpy as np


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

class MainScreen(tk.Frame):
    def __init__(self, master, show_login_screen, add_user, show_user_view_screen):
        super().__init__(master, bg=IFSUL_WHITE)
        self.master = master

        self.show_login_screen = show_login_screen
        self.add_user = add_user
        self.show_user_view_screen = show_user_view_screen


        # Inicializa la variable search_var
        self.search_var = tk.StringVar()


        self.pack(fill="both", expand=True)
        self.create_widgets()

        self.update_chart()  # Muestra el gráfico general al iniciar sin filtros


        # Vincular el evento de cierre de la ventana principal al método on_close
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Banner Verde
        banner_frame = tk.Frame(self, bg=IFSUL_DARK_GREY, height=100, pady=10, padx=35)
        banner_frame.pack(fill="x")






        # Frame principal que contiene tanto los filtros como la gráfica
        self.chart_and_filter_frame = tk.Frame(self, bg=IFSUL_WHITE)
        self.chart_and_filter_frame.pack(side="right", fill="both", expand=True)  # Alineado a la derecha y expandible

        # Frame de filtros (dentro del frame principal)
        self.filter_frame = tk.Frame(self.chart_and_filter_frame, bg=IFSUL_WHITE)
        self.filter_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")  # Filtros arriba

        # Organizar los selectores en una fila
        self.filter_row_frame = tk.Frame(self.filter_frame, bg=IFSUL_WHITE)
        self.filter_row_frame.pack(anchor="w", pady=5)  # Empaquetar en la parte superior, alineado a la izquierda

        # Label de tipo de filtro
        filter_type_label = tk.Label(self.filter_row_frame, text="Filtrar por:", bg=IFSUL_WHITE, font=FONT_MEDIUM)
        filter_type_label.grid(row=0, column=0, padx=5)

        # Filtro de tipo (Género, Edad, Actividad)
        self.filter_type_var = tk.StringVar(value="Todos")  # Valor predeterminado "Todos"
        self.filter_type_menu = tk.OptionMenu(self.filter_row_frame, self.filter_type_var, "Todos", "Género", "Edad", "Actividad", command=self.update_options)
        self.filter_type_menu.config(width=10)  # Establecer un tamaño fijo para el menú
        self.filter_type_menu.grid(row=0, column=1, padx=5)

        # Filtro de valor específico
        self.filter_value_var = tk.StringVar(value="Todos")  # Valor predeterminado "Todos"
        self.filter_value_menu = tk.OptionMenu(self.filter_row_frame, self.filter_value_var, "Todos")  # Inicialmente solo tiene "Todos"
        self.filter_value_menu.config(width=10)  # Establecer un tamaño fijo para el menú
        self.filter_value_menu.grid(row=0, column=2, padx=5)

        # Botón para aplicar el filtro (debajo de los selectores)
        filter_button = ctk.CTkButton(self.filter_row_frame,text="Aplicar Filtro",font=FONT_LARGE, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE,hover_color=IFSUL_HOVER ,width=100, height=30, corner_radius=10, command=self.update_chart)        
        filter_button.grid(row=0, column=3, padx=5)  # Colocamos el botón en la misma fila, pero en la siguiente columna




        # Frame del gráfico (debajo del frame de filtros)
        self.chart_frame = tk.Frame(self.chart_and_filter_frame, bg=IFSUL_WHITE)
        self.chart_frame.grid(row=1, column=0, sticky="nsew")  # Gráfico debajo de los filtros

        # Hacer que el gráfico se expanda para llenar el espacio
        self.chart_and_filter_frame.grid_rowconfigure(1, weight=1)  # Fila del gráfico expansible
        self.chart_and_filter_frame.grid_columnconfigure(0, weight=1)  # Columna expansible







        # Frame para la etiqueta del nombre del administrador, alineada a la derecha
        admin_frame = tk.Frame(banner_frame, bg=IFSUL_DARK_GREY)
        admin_frame.pack(side="top", anchor="ne", padx=10, pady=5)  # Colocado en la parte superior derecha

        # Etiqueta del nombre del administrador
        admin_label = tk.Label(admin_frame, text=f"Administrador: {self.master.admin_name}", bg=IFSUL_DARK_GREY, fg=IFSUL_WHITE, font=("Helvetica", 15, "bold"))
        admin_label.pack()

        # Frame para los botones
        button_frame = tk.Frame(banner_frame, bg=IFSUL_DARK_GREY)
        button_frame.pack(side="bottom", fill="x")  # Ahora se alinea al fondo del banner



        
        # Botón de "Agregar Usuario"
        ctk.CTkButton(button_frame, text="+ Agregar Usuario", command=self.add_user, 
                    fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=200, height=40, corner_radius=10).pack(side="left", padx=10)

        # Botón de "Agregar Actividad"
        ctk.CTkButton(button_frame, text="+ Agregar Actividad", command=self.master.show_activity_screen, 
                    fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=200, height=40, corner_radius=10).pack(side="left", padx=10)

        # Botón de "Salir"
        ctk.CTkButton(button_frame, text="Cerrar Sesión", command=self.logout, 
                    fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=100, height=40,corner_radius=10).pack(side="right", padx=10)




        # Título de la sección de usuarios
        tk.Label(self, text="Usuarios:", bg=IFSUL_WHITE, fg=IFSUL_GREEN, font=("Helvetica", 20, "bold")).pack(side="top", anchor="w", padx=50, pady=30)
        

        # Crear un frame para contener el label y el entry en una sola línea 
        search_frame = tk.Frame(self, bg=IFSUL_WHITE) 
        search_frame.pack(padx=10, pady=10) # Empaquetar con ancla a la izquierda
        # Agrega el Label "Buscar:" al lado del campo de búsqueda
        search_label = tk.Label(search_frame,
            text="Buscar:", bg=IFSUL_WHITE, font=FONT_MEDIUM
        )
        search_label.pack(side=tk.LEFT)
        # Agrega el campo de búsqueda con los parámetros solicitados
        search_entry = ctk.CTkEntry(
            search_frame, 
            textvariable=self.search_var, 
            font=FONT_LARGE, 
            fg_color=IFSUL_WHITE, 
            text_color=IFSUL_BLACK,
            width=390,
            border_color="lightgrey", 
            border_width=2
        )
        search_entry.pack(padx=20,side=tk.LEFT)        
        # Evento que llama a la función de búsqueda cuando cambia el texto
        self.search_var.trace("w", lambda *args: self.update_user_list())



        # Canvas y Scrollbar para el scrollable_frame
        self.canvas = tk.Canvas(self, bg=IFSUL_WHITE)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame para el contenido desplazable
        self.scrollable_frame = tk.Frame(self.canvas, bg=IFSUL_WHITE)
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        # Crear una ventana en el canvas y colocar el scrollable_frame en ella
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")

        # Vincular el evento de scroll del ratón al canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Frame para los usuarios
        self.users_frame = tk.Frame(self.scrollable_frame, bg=IFSUL_WHITE)
        self.users_frame.pack(padx=1, pady=20)
        self.render_users()


        # Vincular el evento de redimensionamiento de la ventana al método para actualizar el tamaño del canvas
        self.master.bind("<Configure>", self.on_window_resize)

    def update_user_list(self):
        # Realiza la búsqueda en la base de datos usando el texto en search_var
        search_text = self.search_var.get()

        # Divide el texto de búsqueda en palabras individuales
        search_words = search_text.split()

        # Conexión a la base de datos y consulta con filtro
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        # Construye la consulta SQL para que cada palabra sea comparada con ambas columnas
        query = """
            SELECT idusuario, idactividad, nome, sobrenome, fecha, email, genero, foto 
            FROM usuario 
            WHERE idAdmin = %s
        """
        
        # Genera condiciones para que cada palabra sea buscada en `nome` y `sobrenome`
        conditions = []
        params = [self.master.current_admin_id]
        
        for word in search_words:
            conditions.append("(nome LIKE %s OR sobrenome LIKE %s)")
            params.extend([f"%{word}%", f"%{word}%"])

        # Añadimos todas las condiciones al query usando `AND` para que todas las palabras tengan que coincidir
        if conditions:
            query += " AND " + " AND ".join(conditions)

        # Ejecuta la consulta
        cursor.execute(query, params)
        users = cursor.fetchall()
        cursor.close()
        connection.close()

        
        # Renderiza los resultados de la búsqueda
        self.render_users(users)
        
    def update_options(self, selection):
        connection = create_connection()
        cursor = connection.cursor()

        options = ["Todos"]  # Opción predeterminada para mostrar el gráfico general

        if selection == "Género":
            cursor.execute("SELECT DISTINCT genero FROM usuario")
            options.extend([row[0] for row in cursor.fetchall()])
        elif selection == "Edad":
            options.extend(["18-25", "26-35", "36-45", "46-60", "60+"])  # Rangos de edad predefinidos
        elif selection == "Actividad":
            cursor.execute("SELECT nombre FROM actividad WHERE idAdmin = %s", (self.master.current_admin_id,))
            options.extend([row[0] for row in cursor.fetchall()])

        cursor.close()
        connection.close()

        # Actualiza las opciones del menú
        self.filter_value_var.set("Todos")  # Valor predeterminado "Todos"
        self.filter_value_menu['menu'].delete(0, 'end')
        for option in options:
            self.filter_value_menu['menu'].add_command(label=option, command=tk._setit(self.filter_value_var, option))

    def update_chart(self):
        # Limpiar gráfico anterior
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        filter_type = self.filter_type_var.get()
        filter_value = self.filter_value_var.get()

        # Consulta base para obtener las emociones promedio
        connection = create_connection()
        cursor = connection.cursor()

        query = """
            SELECT u.idUsuario, 
                AVG(r.ira) AS avg_ira, 
                AVG(r.disgusto) AS avg_disgusto, 
                AVG(r.miedo) AS avg_miedo, 
                AVG(r.feliz) AS avg_feliz,
                AVG(r.neutral) AS avg_neutral, 
                AVG(r.triste) AS avg_triste, 
                AVG(r.sorpresa) AS avg_sorpresa
            FROM usuario u
            LEFT JOIN resultado r ON r.idUsuario = u.idUsuario
            JOIN actividad a ON u.idActividad = a.idActividad
            WHERE u.idAdmin = %s
        """

        params = [self.master.current_admin_id]  # Inicializa parámetros con idAdmin

        # Agregar condiciones según el filtro
        if filter_type == "Género" and filter_value != "Todos":
            query += " AND u.genero = %s"
            params.append(filter_value)
        elif filter_type == "Edad" and filter_value != "Todos":
            if filter_value == "18-25":
                query += " AND FLOOR(DATEDIFF(CURDATE(), u.fecha) / 365) BETWEEN 18 AND 25"
            elif filter_value == "26-35":
                query += " AND FLOOR(DATEDIFF(CURDATE(), u.fecha) / 365) BETWEEN 26 AND 35"
            elif filter_value == "36-45":
                query += " AND FLOOR(DATEDIFF(CURDATE(), u.fecha) / 365) BETWEEN 36 AND 45"
            elif filter_value == "46-60":
                query += " AND FLOOR(DATEDIFF(CURDATE(), u.fecha) / 365) BETWEEN 46 AND 60"
            elif filter_value == "60+":
                query += " AND FLOOR(DATEDIFF(CURDATE(), u.fecha) / 365) > 60"
        elif filter_type == "Actividad" and filter_value != "Todos":
            query += " AND a.nombre = %s"            
            params.append(filter_value)

        cursor.execute(query, params)  # Ejecutar consulta con parámetros

        results = cursor.fetchall()
        cursor.close()
        connection.close()

        if not results or all(all(value is None for value in result[1:]) for result in results):
            no_data_label = tk.Label(self.chart_frame, text="No hay análisis disponibles para mostrar.", bg=IFSUL_WHITE, fg=IFSUL_GREEN, font=FONT_MEDIUM)
            no_data_label.pack(pady=20)            
            return

        # Calcular promedios, reemplazando None por 0
        averages = [np.mean([row[i] if row[i] is not None else 0 for row in results]) for i in range(1, 8)]
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
        fig, ax = plt.subplots(figsize=(4, 2))
        bars = ax.bar(emotions, averages, color=colors)
        ax.set_title("Promedio de Emociones")
        ax.set_ylabel("Promedio")

        # Ajustar el límite superior del eje y
        ax.set_ylim(0, max(averages) + 8)  # Ajustar el límite superior a un valor más alto

        
        # Añadir los porcentajes encima de cada barra
        for bar in bars:
            yval = bar.get_height()
            if yval.is_integer():
                ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{int(yval)}%', ha='center', va='bottom')
            else:
                ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.3f}%', ha='center', va='bottom')


        # Mostrar gráfico en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # Cerrar la figura después de mostrarla
        plt.close(fig)







    def render_users(self, users= None):
        # Limpiar el frame de usuarios antes de renderizar
        for widget in self.users_frame.winfo_children():
            widget.destroy()
        # Si no se pasan usuarios (al cargar la pantalla), obtenemos todos los usuarios.
        if users is None:
            conn = create_connection()
            cursor = conn.cursor(dictionary=True)
            try:
                query = "SELECT idusuario, idactividad, nome, sobrenome, fecha, email, genero, foto FROM usuario WHERE idAdmin = %s"
                cursor.execute(query, (self.master.current_admin_id,))
                users = cursor.fetchall()
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al obtener los usuarios: {e}")
            finally:
                conn.close()

        # Si no hay usuarios, mostramos un mensaje
        if not users:
            tk.Label(self.users_frame, text="No hay usuarios registrados.", bg=IFSUL_WHITE, fg=IFSUL_GREEN, font=FONT_MEDIUM).pack(pady=5)
        else:
            for widget in self.users_frame.winfo_children():
                widget.destroy()

            # Renderiza cada usuario en la interfaz
            for user in users:
                user_frame = tk.Frame(self.users_frame, bg=IFSUL_GREY, width=600, height=150, cursor="hand2", padx=19, pady=15)
                user_frame.pack(pady=20, anchor="center", padx=10, fill="x")
                
                user_frame.bind("<Button-1>", lambda e, user=user: self.view_user(user))

                # Usar grid en el banner para alinear el contenido
                user_frame.grid_rowconfigure(0, weight=1)
                user_frame.grid_columnconfigure(0, weight=1)
                user_frame.grid_columnconfigure(1, weight=0)

                text_frame = tk.Frame(user_frame, bg=IFSUL_GREY)
                text_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

                full_name = f"{user['nome']} {user['sobrenome']}"
                name_label = tk.Label(text_frame, text=full_name, bg=IFSUL_GREY, fg=IFSUL_GREEN, font=("Helvetica", 14, "bold"))
                name_label.pack(anchor="w")
                name_label.bind("<Button-1>", lambda e, user=user: self.view_user(user))

                email_label = tk.Label(text_frame, text=user['email'], bg=IFSUL_GREY, fg=IFSUL_GREEN, font=FONT_MEDIUM)
                email_label.pack(anchor="w")
                email_label.bind("<Button-1>", lambda e, user=user: self.view_user(user))

                if user['foto']:
                    image = Image.open(io.BytesIO(user['foto']))
                    image.thumbnail((150, 150))
                    photo = ImageTk.PhotoImage(image)
                    photo_label = tk.Label(user_frame, image=photo, bg=IFSUL_GREY)
                    photo_label.image = photo  # Mantener una referencia
                    photo_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")
                    photo_label.bind("<Button-1>", lambda e, user=user: self.view_user(user))
            
    


    def view_user(self, user):
        self.master.show_user_view_screen(user)

    def on_frame_configure(self, event):
        # Ajustar el tamaño del canvas para que coincida con el tamaño del contenido
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        # Ajusta el scroll del canvas basado en la rueda del mouse
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_window_resize(self, event):
        if self.canvas is not None and self.canvas_window is not None:
            try:
                self.canvas.itemconfig(self.canvas_window, width=self.canvas.winfo_width())
            except tk.TclError:
                # Maneja el error si el widget ya no existe
                pass    
    
    def logout(self):
        self.master.current_admin_id = None
        # Desvincula el evento de redimensionamiento antes de cerrar la ventana
        self.master.unbind("<Configure>")
        self.show_login_screen()
    
    def on_close(self):  # Agregado para manejar el cierre de la ventana
        if messagebox.askokcancel("Cerrar", "¿Estás seguro de que deseas cerrar la aplicación?"):
            plt.close('all')  # Cerrar cualquier ventana o gráfico activo de Matplotlib

            # Limpiar la sesión de TensorFlow si es necesario
            tf.keras.backend.clear_session()
            # Usar after para dar un pequeño retraso
            self.master.after(100, self.master.quit)
            self.master.after(100, self.master.destroy)
