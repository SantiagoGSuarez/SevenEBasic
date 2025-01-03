import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import customtkinter as ctk  
from database import create_connection

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

class LoginScreen(tk.Frame):
    def __init__(self, master, show_main_screen, show_register_screen):
        super().__init__(master)
        self.master = master
        self.show_main_screen = show_main_screen
        self.show_register_screen = show_register_screen



        self.configure(bg=IFSUL_WHITE)
        self.pack(expand=True, fill="both")
        self.create_widgets()

    def create_widgets(self):

        # Frame principal que contendrá el banner a la izquierda y el login a la derecha
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


        # Frame para el formulario de login a la derecha
        login_frame = tk.Frame(main_container, bg=IFSUL_WHITE)
        login_frame.pack(side="right", expand=True, fill="both")

        container = tk.Frame(login_frame, bg=IFSUL_WHITE)
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="Login", bg=IFSUL_WHITE, fg=IFSUL_GREEN, font=("Helvetica", 24, "bold")).pack(pady=20)
        
        fields_frame = tk.Frame(container, bg=IFSUL_WHITE)
        fields_frame.pack(pady=20, expand=True)


        # Reemplaza los campos Entry de tkinter por CTkEntry
        ctk.CTkLabel(fields_frame, text="Nombre de usuario:",text_color=IFSUL_GREEN, font=FONT_MAX).grid(row=0, column=0, pady=10, sticky="e")
        self.username_entry = ctk.CTkEntry(fields_frame, font=FONT_LARGE, width=200, fg_color=IFSUL_WHITE, text_color=IFSUL_BLACK, border_color="lightgrey",border_width=2)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(fields_frame, text="Contraseña:", text_color=IFSUL_GREEN, font=FONT_MAX).grid(row=1, column=0, pady=10, sticky="e")
        self.password_entry = ctk.CTkEntry(fields_frame, show="*", font=FONT_LARGE, width=200, fg_color=IFSUL_WHITE, text_color=IFSUL_BLACK, border_color="lightgrey",border_width=2)  # Ajustamos el tamaño del campo
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)


        self.show_password_var = tk.IntVar()
        show_password_checkbutton = ctk.CTkCheckBox(fields_frame, 
                                                    text="Mostrar contraseña", 
                                                    variable=self.show_password_var, 
                                                    command=self.toggle_password, 
                                                    text_color=IFSUL_GREEN,  # Color del texto
                                                    fg_color="lightgrey",  # Color de fondo del cuadro de selección
                                                    font=FONT_SMALL, hover_color=IFSUL_HOVER, border_width=2, border_color="lightgrey", checkmark_color=IFSUL_LIGHT_GREEN)
        show_password_checkbutton.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        
        buttons_frame = tk.Frame(container, bg=IFSUL_WHITE)
        buttons_frame.pack(pady=20)

        
        # Reemplaza los botones de tkinter por CTkButton
        ctk.CTkButton(buttons_frame, text="Iniciar sesión", command=self.on_login, font=FONT_LARGE, fg_color=IFSUL_GREEN, text_color=IFSUL_WHITE,hover_color=IFSUL_HOVER ,width=160, height=40, corner_radius=10).pack(pady=5)
        ctk.CTkButton(buttons_frame, text="Registrarse", command=self.show_register_screen, font=FONT_LARGE, fg_color=IFSUL_LIGHT_GREEN, text_color=IFSUL_WHITE, hover_color=IFSUL_HOVER, width=160, height=40, corner_radius=10).pack(pady=5)


    
    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def on_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            conn = create_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM admin WHERE BINARY nome = %s AND BINARY senha = %s"
            cursor.execute(query, (username, password))
            admin = cursor.fetchone()
            conn.close()

            if admin:
                self.master.current_admin_id = admin['idAdmin']
                self.master.admin_name = admin['nome']
                self.show_main_screen()
            else:
                messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos")
        except Exception as e:
            # Si ocurre un error en cualquier parte del proceso (ej. conexión a la base de datos)
            messagebox.showerror("Error", f"Usuario no existe: {str(e)}")
                