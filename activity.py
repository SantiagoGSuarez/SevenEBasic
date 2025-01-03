import tkinter as tk
import customtkinter as ctk  
from PIL import Image, ImageTk
from tkinter import messagebox, simpledialog
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


class ActivityScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=IFSUL_WHITE)

        self.master = master
        


        self.create_widgets()
        
        # Cargar actividades al inicio
        self.load_activities()



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

        ctk.CTkButton(top_banner_frame,text="", image=izquierda_image, command=self.go_back,fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=10, height=40, corner_radius=10).pack(side="left", padx=10)


       
        main_frame = tk.Frame(self, bg=IFSUL_WHITE)
        main_frame.pack(pady=(0, 0), padx=10, expand=True, fill="both")  # Ajustar pady aquí para reducir el espacio

        # Frame para el registro de actividad
        self.register_frame = tk.Frame(main_frame, bg=IFSUL_WHITE)
        self.register_frame.pack(side="top", padx=10, pady=30)  # Reducir el pady inferior a 0

        activities_label = tk.Label(self.register_frame, text="Registrar Actividad", bg=IFSUL_WHITE, fg=IFSUL_GREEN, font=("Helvetica", 20, "bold"))
        activities_label.pack(pady=(10, 5))

        self.activity_entry = tk.Entry(self.register_frame, font=FONT_MEDIUM, width=30)
        self.activity_entry.pack(pady=(0, 5))

        create_button = ctk.CTkButton(self.register_frame, text="Registrar", command=self.create_activity, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, height=40, corner_radius=10)
        create_button.pack()

        # Frame gris para la lista de actividades, ubicado debajo del frame de registro
        self.activities_frame = tk.Frame(main_frame, bg=IFSUL_GREY)
        self.activities_frame.pack(side="top", fill="y", expand=True, pady=(0, 10))  # Ajustar el pady aquí

        self.activities_frame.pack_propagate(False)
        self.activities_frame.config(width=470)

        self.activities_label = tk.Label(self.activities_frame, text="Listado de Actividades", bg=IFSUL_GREY, fg=IFSUL_GREEN, font=("Helvetica", 20, "bold"))
        self.activities_label.pack(pady=(5, 5))  # Mantener o ajustar el pady según sea necesario

        self.frame = tk.Frame(main_frame, bg=IFSUL_WHITE)
        self.frame.pack(side="top", fill="y")  # Ajustar el pady aquí

        self.no_activity_label = tk.Label(self.frame, text="No hay actividades registradas.", bg=IFSUL_WHITE, fg="red", font=FONT_MEDIUM)
        self.no_activity_label.pack_forget()

        self.canvas = tk.Canvas(self.activities_frame, bg=IFSUL_GREY)
        self.canvas.pack(side="left", fill="both", expand=True)

        

        self.scrollbar = tk.Scrollbar(self.activities_frame, command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_container = tk.Frame(self.canvas, bg=IFSUL_GREY, padx=10)
        self.scrollable_container.bind("<Configure>", self.on_frame_configure)
        self.canvas.create_window((0, 0), window=self.scrollable_container, anchor="nw")

        self.scrollable_frame = tk.Frame(self.scrollable_container, bg=IFSUL_GREY)
        self.scrollable_frame.pack(fill="both", expand=True)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    






    def load_activities(self):


        # Limpiar el frame de actividades antes de cargar nuevas actividades
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT idActividad, nombre FROM actividad WHERE idAdmin = %s", (self.master.current_admin_id,))
        activities = cursor.fetchall()
        connection.close()

        # Si no hay actividades, mostrar mensaje de no actividades
        if not activities:
            self.no_activity_label.pack()
        else:
            # Ocultar la etiqueta de no actividades
            self.no_activity_label.pack_forget()

            # Crear una etiqueta para cada actividad
            for idx, activity in enumerate(activities):
                activity_id, activity_name = activity

                # Crear un frame para cada actividad
                activity_frame = tk.Frame(self.scrollable_frame, bg=IFSUL_GREY)
                activity_frame.pack(fill="x", padx=10, pady=5)

                # Etiqueta de la actividad alineada a la izquierda
                activity_label = tk.Label(activity_frame, text=activity_name, bg=IFSUL_GREY, font=FONT_MEDIUM)
                activity_label.pack(side="left", padx=(0, 10), anchor="w")
                

                # Cargar las imágenes para los botones
                editar_image = ctk.CTkImage(Image.open("Resources/editar.png"), size=(25, 25))
                eliminar_image = ctk.CTkImage(Image.open("Resources/eliminar.png"), size=(25, 25))


                # Botón de eliminar alineado a la derecha
                delete_button = ctk.CTkButton(activity_frame, text="",image=eliminar_image, command=lambda a=activity_id: self.delete_activity(a),fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=10, height=30, corner_radius=10)
                delete_button.pack(side="right", padx=(5, 0))
                
                # Botón de editar alineado a la derecha (primero)
                edit_button = ctk.CTkButton(activity_frame, text="",image=editar_image, command=lambda a=activity_id, name=activity_name: self.open_edit_activity_window(a, name), fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, font=FONT_LARGE,hover_color=IFSUL_HOVER, width=10, height=30, corner_radius=10)
                edit_button.pack(side="right", padx=(5, 0))

                


        # Actualizar el canvas después de cargar las actividades
        self.update_canvas()

    def create_activity(self):
        activity_name = self.activity_entry.get().strip()
        if activity_name:
            connection = create_connection()
            cursor = connection.cursor()

            # Verificar si el nombre ya existe
            cursor.execute("SELECT COUNT(*) FROM actividad WHERE nombre = %s AND idAdmin = %s", (activity_name, self.master.current_admin_id))
            count = cursor.fetchone()[0]

            if count > 0:
                messagebox.showerror("Error", f"La actividad '{activity_name}' ya existe. Por favor, elige otro nombre.")
            else:
                cursor.execute("INSERT INTO actividad (nombre, idAdmin) VALUES (%s, %s)", (activity_name, self.master.current_admin_id))
                connection.commit()
                messagebox.showinfo("Éxito", f"La actividad '{activity_name}' ha sido creada con éxito.")
            
            connection.close()
            self.activity_entry.delete(0, tk.END)
            self.load_activities()
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre para la actividad.")

    def open_edit_activity_window(self, activity_id, old_name):
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Editar Actividad")
        edit_window.iconbitmap("Resources/icono4.ico")
        edit_window.geometry("400x200")
        edit_window.configure(bg=IFSUL_GREY)

        # Centrar la ventana
        self.center_window(edit_window, 400, 200)

        label = tk.Label(edit_window, text="Editar Actividad", font=FONT_MEDIUM, bg=IFSUL_GREY, fg=IFSUL_GREEN)
        label.pack(pady=10)

        entry = ctk.CTkEntry(edit_window, font=FONT_LARGE,fg_color=IFSUL_WHITE, text_color=IFSUL_BLACK, border_color="lightgrey",border_width=2, width=300)
        entry.insert(0, old_name)
        entry.pack(pady=10)

        button_frame = tk.Frame(edit_window, bg=IFSUL_GREY)
        button_frame.pack(pady=10)

        save_button = ctk.CTkButton(button_frame, text="Aceptar", command=lambda: self.save_edit(activity_id, entry.get(), edit_window), font=FONT_LARGE, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE,hover_color=IFSUL_HOVER ,width=80, height=40, corner_radius=10)
        save_button.pack(side="left", padx=5)

        cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=edit_window.destroy, font=FONT_LARGE, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE,hover_color=IFSUL_HOVER ,width=80, height=40, corner_radius=10)
        cancel_button.pack(side="left", padx=5)

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def save_edit(self, activity_id, new_name, window):
        new_name = new_name.strip()  # Quitar espacios al inicio y al final
        if new_name:
            connection = create_connection()
            cursor = connection.cursor()

            # Verificar si el nuevo nombre ya existe en otra actividad
            cursor.execute("SELECT COUNT(*) FROM actividad WHERE nombre = %s AND idActividad != %s", (new_name, activity_id))
            count = cursor.fetchone()[0]

            if count > 0:
                messagebox.showerror("Error", f"El nombre '{new_name}' ya existe. Por favor, elige otro nombre.")
            else:
                # Actualizar el nombre si no hay duplicados
                cursor.execute("UPDATE actividad SET nombre = %s WHERE idActividad = %s", (new_name, activity_id))
                connection.commit()
                messagebox.showinfo("Éxito", "La actividad ha sido editada con éxito.")
                window.destroy()

            connection.close()
            self.load_activities()
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre válido.")

    def delete_activity(self, activity_id):
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar esta actividad?"):
            try:
                connection = create_connection()
                cursor = connection.cursor()

                # Actualiza los usuarios que tienen asignada la actividad
                cursor.execute("UPDATE usuario SET idActividad = NULL WHERE idActividad = %s", (activity_id,))
                connection.commit()

                # Ahora elimina la actividad
                cursor.execute("DELETE FROM actividad WHERE idActividad = %s", (activity_id,))
                connection.commit()

                messagebox.showinfo("Éxito", "La actividad ha sido eliminada con éxito.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al intentar eliminar la actividad: {e}")
            finally:
                cursor.close()
                connection.close()
                self.load_activities()

    def update_canvas(self):
        # Establecer el área de desplazamiento del canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_frame_configure(self, event):
        self.update_canvas()
        # Establecer el área de desplazamiento del canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    
    def go_back(self):
        self.master.show_main_screen()  # Asumiendo que tienes esta función en la clase principal

    def on_close(self):
        # Muestra un mensaje de confirmación antes de cerrar la ventana
        if messagebox.askokcancel("Cerrar", "¿Estás seguro de que deseas cerrar la aplicación?"):
            # Limpiar la sesión de TensorFlow si es necesario
            tf.keras.backend.clear_session()
            self.master.quit()  # Finaliza el mainloop de Tkinter
            self.master.destroy()  # Cerrar la ventana principal