import sqlalchemy as db 
from sqlalchemy import exc
import persistence.model as mod
from persistence.model import *
import mysql.connector
from persistence.repository.database_manager import DatabaseManager
#este módulo creará nuestra base de datos 

#engine = db.create_engine('sqlite:///./db/login.db', echo = True, future = False)
def create_database():
    try:
        connection = mysql.connector.connect(
            user = 'root',
            password = '1234', # aqui la contraseña
            host = '127.0.0.1',
            #database = 'db_librerio',
            port = '3306'
        )
        cursor = connection.cursor() # para poder crear consultas sql
        cursor.execute("CREATE DATABASE IF NOT EXISTS db_librerio")
        connection.commit()

        #cursor.execute("CREATE USER IF NOT EXISTS 'usuario'@'localhost' IDENTIFIED BY 'contraseña'")
        #cursor.execute("GRANT ALL PRIVILEGES ON db_librerio.* TO 'usuario'@'localhost'")
        #connection.commit()
        print("Base de datos creada con éxito")
    except mysql.connector.Error as error:
        print(f"Error al crear la base de datos: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def build_db():
    try:
        #engine = db.create_engine(f'mysql://{usuario}:{passw}@localhost/{db_usuario}')
        engine = db.create_engine('mysql://root:1234@localhost/db_librerio')
        mod.Base.metadata.create_all(engine)
        print("Base de datos levantada con éxito.")
    except exc.SQLAlchemyError as error: 
        print(f"Error al levantar la base de datos: {error}")

# introducir datos básicos que necesita la aplicación para funcionar desde el principio
def insert_data():
    database_manager = DatabaseManager()

    # FORMATOS 
    formato_fisico = Formato()
    formato_fisico.id = 1000 # el formato físico tiene id 1000
    formato_fisico.tipo = "Físico"
    formato_pdf = Formato()
    formato_pdf.id = 1001 # el formato pdf tiene id 1001
    formato_pdf.tipo = "PDF"

    database_manager.insertFormato(formato_fisico)
    database_manager.insertFormato(formato_pdf)

    # GÉNEROS
    genero_no_ficcion = Genero()
    genero_no_ficcion.nombre = "No ficción"
    genero_ficcion = Genero()
    genero_ficcion.nombre = "Ficción"
    genero_poesia = Genero()
    genero_poesia.nombre = "Poesía"
    genero_otro = Genero()
    genero_otro.nombre = "Otro"

    database_manager.insertGenero(genero_no_ficcion)
    database_manager.insertGenero(genero_ficcion)
    database_manager.insertGenero(genero_poesia)
    database_manager.insertGenero(genero_otro)

    # CATEGORÍAS
    categoria_fantasia = Categoria()
    categoria_fantasia.nombre = "Fantasía"
    categoria_fantasia.nombre_genero = "Ficción"
    categoria_ciencia_ficcion = Categoria()
    categoria_ciencia_ficcion.nombre = "Ciencia ficción"
    categoria_ciencia_ficcion.nombre_genero = "Ficción"
    categoria_manga = Categoria()
    categoria_manga.nombre = "Manga"
    categoria_manga.nombre_genero = "Ficción"
    categoria_policiaca = Categoria()
    categoria_policiaca.nombre = "Novela policiaca"
    categoria_policiaca.nombre_genero = "No ficción"
    categoria_historica = Categoria()
    categoria_historica.nombre = "Novela histórica"
    categoria_historica.nombre_genero = "No ficción"
    categoria_ensayo = Categoria()
    categoria_ensayo.nombre = "Ensayo"
    categoria_ensayo.nombre_genero = "No ficción"

    database_manager.insertCategoria(categoria_fantasia)
    database_manager.insertCategoria(categoria_ciencia_ficcion)
    database_manager.insertCategoria(categoria_historica)
    

create_database() # creamos la base de datos
build_db() # levantamos la base de datos
insert_data() # introducimos datos básicos