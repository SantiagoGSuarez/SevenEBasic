import mysql.connector
from mysql.connector import errorcode

# Configuración de la base de datos sin especificar 'database'
db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'port': 3306
}

database_name = 'tcc_deteccion_emociones'


def create_connection(db=None):
    """Crea una conexión a MySQL, opcionalmente especificando una base de datos."""
    config = db_config.copy()  # Copiar la configuración
    if db:
        config['database'] = db  # Especificamos la base de datos si es necesario
    return mysql.connector.connect(**config)


def initialize_database():
    """Verifica si la base de datos existe; si no, la crea junto con sus tablas."""
    connection = None
    cursor = None
    try:
        # Conectarse sin especificar la base de datos (sin el campo 'database')
        connection = create_connection()  # Conexión sin base de datos
        cursor = connection.cursor()

        # Verificar si la base de datos 'tcc_deteccion_emociones' existe
        cursor.execute(f"SHOW DATABASES LIKE '{database_name}';")
        db_exists = cursor.fetchone() is not None

        if not db_exists:
            # Crear la base de datos si no existe
            print(f"Creando la base de datos '{database_name}'...")
            cursor.execute(f"CREATE DATABASE {database_name} DEFAULT CHARACTER SET 'utf8mb4';")
            print(f"Base de datos '{database_name}' creada exitosamente.")

        # Cerrar la conexión sin base de datos
        cursor.close()
        connection.close()

        # Ahora, reconectamos especificando la base de datos creada
        # Modificamos la configuración para incluir la base de datos
        db_config['database'] = database_name  # Aquí agregamos el campo 'database'

        # Conectar de nuevo con la base de datos ahora que sabemos que existe
        connection = create_connection(database_name)
        cursor = connection.cursor()

        # Crear las tablas necesarias si no existen
        create_tables(cursor)
        print("Tablas verificadas/creadas correctamente.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error de autenticación. Verifica el usuario y la contraseña.")
        else:
            print(f"Error de MySQL: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def create_tables(cursor):
    """Crea las tablas necesarias si no existen."""
    tables = {
        "admin": """
            CREATE TABLE IF NOT EXISTS admin (
                idAdmin INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50) NOT NULL,
                email VARCHAR(255) NOT NULL,
                senha VARCHAR(255) NOT NULL
            )
        """,
        "actividad": """
            CREATE TABLE IF NOT EXISTS actividad (
                idActividad INT AUTO_INCREMENT PRIMARY KEY,
                idAdmin INT DEFAULT NULL,
                nombre VARCHAR(255) NOT NULL,
                FOREIGN KEY (idAdmin) REFERENCES admin(idAdmin)
            )
        """,
        "usuario": """
            CREATE TABLE IF NOT EXISTS usuario (
                idUsuario INT AUTO_INCREMENT PRIMARY KEY,
                idAdmin INT NOT NULL,
                idActividad INT DEFAULT NULL,
                nome VARCHAR(50) NOT NULL,
                sobrenome VARCHAR(50) NOT NULL,
                fecha DATE NOT NULL,
                genero VARCHAR(50) NOT NULL,
                email VARCHAR(255) NOT NULL,
                foto LONGBLOB NOT NULL,
                FOREIGN KEY (idAdmin) REFERENCES admin(idAdmin),
                FOREIGN KEY (idActividad) REFERENCES actividad(idActividad)
            )
        """,
        "resultado": """
            CREATE TABLE IF NOT EXISTS resultado (
                idResultado INT AUTO_INCREMENT PRIMARY KEY,
                idUsuario INT NOT NULL,
                fecha_hora DATETIME NOT NULL,
                duracion TIME NOT NULL,
                ira FLOAT NOT NULL,
                disgusto FLOAT NOT NULL,
                miedo FLOAT NOT NULL,
                feliz FLOAT NOT NULL,
                neutral FLOAT NOT NULL,
                triste FLOAT NOT NULL,
                sorpresa FLOAT NOT NULL,
                FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario)
            )
        """
    }

    for table_name, table_creation_query in tables.items():
        print(f"Verificando/Creando tabla '{table_name}'...")
        cursor.execute(table_creation_query)
