import subprocess
import sys
import os
import socket

def check_internet_connection():
    """Verifica si hay conexión a Internet intentando conectarse al DNS público de Google."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)  # Conexión al DNS público de Google
        return True
    except OSError:
        return False

def install_requirements():
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} no encontrado.")
        return  # No detener la ejecución, solo mostrar el mensaje

    internet_available = check_internet_connection()

    try:
        # Intentar actualizar pip si hay conexión a Internet
        if internet_available:
            print("Actualizando pip...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            print("pip actualizado correctamente.\n")
        else:
            print("Advertencia: No hay conexión a Internet. No se pudo actualizar pip.")
        
        # Verificar si ya están instaladas todas las bibliotecas
        print("Verificando bibliotecas necesarias...")
        with open(requirements_file, "r") as file:
            libraries = file.readlines()
        missing_libraries = []
        for library in libraries:
            library_name = library.strip().split("==")[0]
            try:
                __import__(library_name)
            except ImportError:
                missing_libraries.append(library.strip())

        if not missing_libraries:
            print("ESTAS SON LAS BIBLIOTECAS NECESARIAS:")
            print("\n".join(libraries))
            print("¡Todas las bibliotecas están instaladas!")
        else:
            if internet_available:
                print("Faltan algunas bibliotecas, instalando ahora...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
                print("¡Instalación completa!")
            else:
                print("Advertencia: No hay conexión a Internet. No se pudieron instalar las siguientes bibliotecas:")
                print("\n".join(missing_libraries))
    except subprocess.CalledProcessError:
        print("Error: Ocurrió un problema al instalar bibliotecas o actualizar pip.")
        print("Asegúrese de verificar la configuración de su red o instalar manualmente las bibliotecas faltantes.")
    except Exception as e:
        print(f"Error inesperado durante la instalación de bibliotecas: {e}")

# Instalar requisitos antes de ejecutar la aplicación
install_requirements()




import tkinter as tk
from login import LoginScreen  
from register import RegisterScreen
from main_screen import MainScreen
from user_register import UserRegisterScreen
from view_user import ViewUserScreen
from modify_user import ModifyUserScreen
from internal_analysis import InternalAnalysisScreen
from external_analysis import ExternalAnalysisScreen
from results_screen import ResultsScreen
from view_results import ViewResultsScreen
from result import ResultScreen
from activity import ActivityScreen
from database import initialize_database

# Colores de la paleta de IFSUL
IFSUL_GREEN = "#006400"
IFSUL_LIGHT_GREEN = "#00A36C"
IFSUL_WHITE = "#FFFFFF" #o F4F4F4
IFSUL_DARK_GREY = "#2F4F4F"

# Tamaño de fuente global
FONT_LARGE = ("Helvetica", 16)
FONT_MEDIUM = ("Helvetica", 14)
FONT_SMALL = ("Helvetica", 12)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Detección y Análisis de Expresiones Faciales")
        self.geometry("1280x800")
        self.minsize(800, 700)
        self.iconbitmap("Resources/icono4.ico")
        self.configure(bg=IFSUL_WHITE)
        self.current_admin_id = None
        self.update_idletasks()
        self.center_window(1280, 800)
        self.show_login_screen()

    def center_window(self, width, height):
        # Obtiene las dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calcula la posición x, y para centrar la ventana
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        # Establece la geometría de la ventana
        self.geometry(f"{width}x{height}+{x}+{y}")

    def show_login_screen(self):
        self.clear_frame()
        self.login_screen = LoginScreen(self, self.show_main_screen, self.show_register_screen)  # Pasar el método show_register_screen
        self.login_screen.pack(fill="both", expand=True)
        self.update_idletasks()

    def show_register_screen(self):
        self.clear_frame()
        self.register_screen = RegisterScreen(self, self.show_login_screen)
        self.register_screen.pack(fill="both", expand=True)
        self.update_idletasks()

    def show_main_screen(self):
        self.clear_frame()
        self.main_screen = MainScreen(self, self.show_login_screen, self.show_user_register_screen, self.show_user_view_screen)
        self.main_screen.pack(fill="both", expand=True)
        self.update_idletasks()


    def show_user_register_screen(self):
        self.clear_frame()
        self.user_register_screen = UserRegisterScreen(self, self.show_main_screen)
        self.user_register_screen.pack(fill="both", expand=True)

    def show_user_view_screen(self, user_data):
        self.clear_frame()
        self.user_view_screen = ViewUserScreen(self, user_data, self.show_internal_analysis_screen, self.show_external_analysis_screen)
        self.user_view_screen.pack(fill="both", expand=True)
        self.update_idletasks()
    
    def show_modify_user_screen(self, user_data):
        self.clear_frame()
        self.modify_user_screen = ModifyUserScreen(self, user_data)
        self.modify_user_screen.pack(fill="both", expand=True)
        self.update_idletasks()
    
    def show_internal_analysis_screen(self, user_data):
        self.clear_frame()
        self.internal_analysis_screen = InternalAnalysisScreen(self, user_data)
        self.internal_analysis_screen.pack(fill="both", expand=True)
        self.update_idletasks()

    def show_external_analysis_screen(self, user_data):
        self.clear_frame()
        self.external_analysis_screen = ExternalAnalysisScreen(self, user_data)
        self.external_analysis_screen.pack(fill="both", expand=True)
        self.update_idletasks()

    def show_results_screen(self, user_data, results):
        self.clear_frame()
        self.results_screen = ResultsScreen(self, user_data, results)
        self.results_screen.pack(fill="both", expand=True)
        self.update_idletasks()

    def show_view_results_screen(self, user_data):
        self.clear_frame()
        self.view_results_screen = ViewResultsScreen(self, user_data)
        self.view_results_screen.pack(fill="both", expand=True)
        self.update_idletasks()

    def show_result_screen(self, id_resultado ,user_data):
        self.clear_frame()
        self.result_screen = ResultScreen(self, id_resultado ,user_data)
        self.result_screen.pack(fill="both", expand=True)
        self.update_idletasks()

    def show_activity_screen(self):
        self.clear_frame()
        self.activity_screen = ActivityScreen(self)
        self.activity_screen.pack(fill="both", expand=True)
        self.update_idletasks()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    print("Inicializando base de datos...")
    initialize_database()  # Verifica y crea la base de datos y tablas
    app = Application()
    app.mainloop()
