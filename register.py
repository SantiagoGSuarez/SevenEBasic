import tkinter as tk
import customtkinter as ctk  
from tkinter import messagebox
from PIL import Image, ImageTk
from database import create_connection
import mysql.connector  
import re  

# Colores de la paleta de IFSUL
IFSUL_GREEN = "#006400"
IFSUL_LIGHT_GREEN = "#00A36C"
IFSUL_WHITE = "#FFFFFF" #o F4F4F4
IFSUL_DARK_GREY = "#2F4F4F"
IFSUL_BLACK = "#000000"
IFSUL_HOVER = "#04ca88"

# Tamaño de fuente global
FONT_MAX = ("Helvetica", 19)
FONT_LARGE = ("Helvetica", 16)
FONT_MEDIUM = ("Helvetica", 14)
FONT_SMALL = ("Helvetica", 12)

class RegisterScreen(tk.Frame):
    def __init__(self, master, show_login_screen):
        super().__init__(master)
        self.master = master
        self.show_login_screen = show_login_screen
        

        self.configure(bg=IFSUL_WHITE)
        self.pack(expand=True, fill="both")
        self.create_widgets()
        

    def create_widgets(self):

       # Frame principal que contendrá el banner a la izquierda y el registro a la derecha
        main_container = tk.Frame(self, bg=IFSUL_WHITE)
        main_container.pack(expand=True, fill="both")

        # Frame para el banner en el lado izquierdo
        banner_frame = tk.Frame(main_container, bg=IFSUL_GREEN, width=200)
        banner_frame.pack(side="left", fill="y")

        # Cargar y mostrar la imagen en el banner
        image_path = "Resources/BannerLR.png"
        image = Image.open(image_path)
        
        image = image.resize((300, 300))  # Ajusta el tamaño de la imagen según sea necesario
        self.banner_image = ImageTk.PhotoImage(image)

        tk.Label(banner_frame, image=self.banner_image, bg=IFSUL_GREEN).pack(padx=0.1, pady=0.1)

        # Frame para el formulario de registro a la derecha
        register_frame = tk.Frame(main_container, bg=IFSUL_WHITE)
        register_frame.pack(side="right", expand=True, fill="both")

        container = tk.Frame(register_frame, bg=IFSUL_WHITE)
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="Registro de Administrador", bg=IFSUL_WHITE, fg=IFSUL_GREEN, font=("Helvetica", 24, "bold")).pack(pady=20)

        # Frame para los campos de entrada
        fields_frame = tk.Frame(container, bg=IFSUL_WHITE)
        fields_frame.pack(pady=20)

        # Reemplaza los campos Entry de tkinter por CTkEntry
        ctk.CTkLabel(fields_frame, text="Nombre de usuario:", text_color=IFSUL_GREEN, font=FONT_MAX).grid(row=0, column=0, pady=10, sticky="e")
        self.reg_username_entry = ctk.CTkEntry(fields_frame, font=FONT_LARGE, width=200, fg_color=IFSUL_WHITE, text_color=IFSUL_BLACK, border_color="lightgrey", border_width=2)  # Ajustamos el tamaño del campo
        self.reg_username_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(fields_frame, text="Email:", text_color=IFSUL_GREEN, font=FONT_MAX).grid(row=1, column=0, pady=10, sticky="e")
        self.reg_email_entry = ctk.CTkEntry(fields_frame, font=FONT_LARGE, width=200, fg_color=IFSUL_WHITE, text_color=IFSUL_BLACK, border_color="lightgrey", border_width=2)  # Ajustamos el tamaño del campo
        self.reg_email_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(fields_frame, text="Contraseña:", text_color=IFSUL_GREEN, font=FONT_MAX).grid(row=2, column=0, pady=10, sticky="e")
        self.reg_password_entry = ctk.CTkEntry(fields_frame, show="*", font=FONT_LARGE, width=200, fg_color=IFSUL_WHITE, text_color=IFSUL_BLACK, border_color="lightgrey", border_width=2)  # Ajustamos el tamaño del campo
        self.reg_password_entry.grid(row=2, column=1, padx=10, pady=10)

        # Checkbutton para mostrar/ocultar la contraseña
        self.show_password_var = tk.IntVar()
        show_password_checkbutton = ctk.CTkCheckBox(fields_frame, 
                                                    text="Mostrar contraseña", 
                                                    variable=self.show_password_var, 
                                                    command=self.toggle_password, 
                                                    text_color=IFSUL_GREEN,  # Color del texto
                                                    fg_color="lightgrey",  # Color de fondo del cuadro de selección
                                                    font=FONT_SMALL, 
                                                    hover_color=IFSUL_HOVER, 
                                                    border_width=2, 
                                                    border_color="lightgrey", 
                                                    checkmark_color=IFSUL_LIGHT_GREEN)
        show_password_checkbutton.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Frame para los botones
        buttons_frame = tk.Frame(container, bg=IFSUL_WHITE)
        buttons_frame.pack(pady=20)

        # Reemplaza los botones de tkinter por CTkButton
        ctk.CTkButton(buttons_frame, text="Registrarse", command=self.on_register, font=FONT_LARGE, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE, hover_color=IFSUL_HOVER, width=160, height=40, corner_radius=10).pack(pady=5)
        ctk.CTkButton(buttons_frame, text="Volver al Login", command=self.show_login_screen, font=FONT_LARGE, fg_color=IFSUL_LIGHT_GREEN, text_color=IFSUL_WHITE, hover_color=IFSUL_HOVER, width=160, height=40,corner_radius=10).pack(pady=5)

    def toggle_password(self):
        if self.show_password_var.get():
            self.reg_password_entry.configure(show="")
        else:
            self.reg_password_entry.configure(show="*")
    
    def validate_email(self, email):
        """Valida si el email tiene el formato correcto"""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def on_register(self):
        username = self.reg_username_entry.get()
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()

        if not username or not email or not password:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "El formato del email no es válido")
            return

        conn = create_connection()
        cursor = conn.cursor()
        try:
            # Consulta para verificar si el nombre de usuario o el correo electrónico ya existen
            check_query = "SELECT COUNT(*) FROM admin WHERE nome = %s OR email = %s"
            cursor.execute(check_query, (username, email))
            result = cursor.fetchone()

            if result[0] > 0:
                messagebox.showerror("Error", "Ya existe un usuario con ese nombre o correo electrónico")
                return

            # Inserción si no existe un usuario duplicado
            query = "INSERT INTO admin (nome, email, senha) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, password))
            conn.commit()
            messagebox.showinfo("Éxito", "Administrador registrado exitosamente")

            self.reg_username_entry.delete(0, tk.END)
            self.reg_email_entry.delete(0, tk.END)
            self.reg_password_entry.delete(0, tk.END)

            self.show_login_screen()
        except mysql.connector.Error as err:
            conn.rollback()
            messagebox.showerror("Error", f"Error al registrar el administrador: {err}")
        finally:
            conn.close()
