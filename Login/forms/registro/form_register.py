from forms.registro.form_designer import FormRegisterDesigner
from persistence.repository.database_manager import DatabaseManager
from persistence.model import *
from tkinter import messagebox
import tkinter as tk
from forms.registro.Conexion import *
import sqlalchemy as db 
import persistence.model as mod
import hashlib
import os 
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import ssl

#------------------------- LÓGICA REGISTRO---------------------------------
class FormRegister(FormRegisterDesigner):
    def __init__(self):
        self.database_manager = DatabaseManager()
        super().__init__()
    
    def register(self):
        if self.isConfirmationPassword():
            usuario = Usuario() 
            usuario.nombre = self.usuario.get() # obtenemos el usuario
            usuario.password = self.passw.get() # obtenemos la contraseña
            usuario.correo = self.email.get() # obtenemos el correo

            if usuario.nombre == "" or usuario.password == "" or usuario.correo == "": # si falta algún campo
                messagebox.showerror(message = "Faltan campos, por favor rellena todos los campos.", title = "Mensaje")
            #self.database_manager = DatabaseManager(usuario.nombre, usuario.password, db_usuario)
            
            elif not(self.isUserRegister(usuario)): # si el usuario no estaba registrado anteriormente
                usuario.password = self.do_hash(self.passw.get()) #cript_dec.encrypted(self.passw.get())
                self.database_manager.insertUser(usuario) # insertamos usuario en la tabla de usuarios registrados y creamos el usuario en la base de datos
                messagebox.showinfo(message = f"Usuario registrado correctamente con correo {usuario.correo}.", title = "Mensaje")
                self.ventana.destroy()
                #self.send_correo(usuario) # enviar correo confirmación

    def do_hash(self, texto: str):
        hasher = hashlib.sha3_512()
        hasher.update(texto.encode('utf-8'))
        return hasher.hexdigest() 

    def isConfirmationPassword(self):
        status: bool = True
        if self.passw.get() != self.passw_conf.get():
            status = False
            messagebox.showerror(message = "Las contraseñas no coinciden, revisa el registro.", title = "Mensaje")
            self.passw.delete(0, tk.END)
            self.passw_conf.delete(0, tk.END)
        return status
        
    def isUserRegister(self, user: Usuario):
        status: bool = False
        usuarios_registrados = self.database_manager.getUsers()
        for usu in usuarios_registrados: 
            if user.id == usu.id:
                status = True
                messagebox.showerror(message = "Usuario ya registrado.", title = "Mensaje")
        return status

    def send_correo(self, usuario: Usuario):
        load_dotenv()
        password = os.getenv("PASSWORD")
        email_sender = "libreriocontacto@gmail.com"
        email_receiver = usuario.correo
        subject = "Confirmación de registro"
        body = f"Bienvenido a la comunidad de Librerio, {usuario.nombre}!!! Esperamos que puedas disfrutar de la aplicación"

        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["Subject"] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as smtp:
            smtp.login(email_sender, password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    # POR AHORA NO SE USA
    def create_database(self, usuario: Usuario):
        try:
            #db_usuario = f'db_{usuario.nombre}_{usuario.id}'
            #nombre = usuario.nombre
            #passw = usuario.password
            #db_usuario = f'db_{usuario.nombre}_{usuario.id}' # definimos el nombre de la base de datos -> db_nombreUsuario_idUsuario

            # creamos la base de datos para el usuario
            #engine = db.create_engine(f'mysql://{nombre}:{passw}@localhost/{db_usuario}')
            engine = db.create_engine('mysql://librerio:1234@localhost/db_librerio')
            mod.Base.metadata.create_all(engine)

            #con = CConexion.ConexionBaseDeDatos(usuario, passw, db_usuario)
            #cursor = con.cursor()
            create_table_usuario = f"""
                    CREATE TABLE IF NOT EXISTS db_librerio.usuario(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(50) NOT NULL,
                        password VARCHAR(20) NOT NULL,
                        correo VARCHAR(100) NOT NULL
                    );
            """
            #cursor.execute(create_table_usuario)
            #con.commit()

            create_table_cuenta = f"""
                    CREATE TABLE IF NOT EXISTS db_librerio.cuenta(
                        usuario INT PRIMARY KEY, 
                        fecha_creacion DATE, 
                        CONSTRAINT fk_cuenta_usuario FOREIGN KEY (usuario) REFERENCES usuario(id)
                    );
            """
            #cursor.execute(create_table_cuenta)
            #con.commit()

            create_table_biblioteca = f"""
                    CREATE TABLE IF NOT EXISTS db_librerio.biblioteca(
                        propietario INT PRIMARY KEY,
                        fecha_creacion DATE, 
                        CONSTRAINT fk_biblioteca_propietario FOREIGN KEY (propietario) REFERENCES usuario(id)
                    );
            """
            #cursor.execute(create_table_biblioteca)
            #con.commit()

            create_table_estante = f"""
                    CREATE TABLE IF NOT EXISTS db_librerio.estante (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        propietario INT,
                        tematica VARCHAR(50),
                        tamano INT NOT NULL, 
                        fecha_creacion DATE, 
                        fecha_modificacion DATE, 
                        tipo ENUM('LIBROS', 'OTROS', 'LIBROS/OTROS'),
                        CONSTRAINT fk_estante_propietario FOREIGN KEY (propietario) REFERENCES usuario(id)
                    );
            """
            #cursor.execute(create_table_estante)
            #con.commit()

            create_table_formato = f"""
                    CREATE TABLE IF NOT EXISTS db_librerio.formato(
                        id INT PRIMARY KEY, 
                        tipo VARCHAR(20) NOT NULL
                    );
            """
            #cursor.execute(create_table_formato)
            #con.commit()

            create_table_documento = f"""
                    CREATE TABLE IF NOT EXISTS db_librerio.documento(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        titulo VARCHAR(100) NOT NULL,
                        autor VARCHAR(100),
                        formato INT, 
                        CONSTRAINT fk_documento FOREIGN KEY (formato) REFERENCES formato(id)
                    );
            """
            #cursor.execute(create_table_documento)
            #con.commit()

            create_table_genero = f"""
                    CREATE TABLE IF NOT EXISTS db_librerio.genero(
                        nombre VARCHAR(50) PRIMARY KEY
                    );
            """
            #cursor.execute(create_table_genero)
            #con.commit()

            create_table_categoria = f"""
                    CREATE TABLE IF NOT EXISTS db_librerio.categoria(
                        nombre VARCHAR(50) PRIMARY KEY, 
                        genero VARCHAR(50),
                        CONSTRAINT fk_categoria_genero FOREIGN KEY (genero) REFERENCES genero(nombre)
                    );
            """
            #cursor.execute(create_table_categoria)
            #con.commit()

            create_table_libro = f"""
                    CREATE TABLE IF NOT EXISTS db_librerio.libro(
                        isbn INT,
                        id INT, 
                        fecha_publicacion DATE,
                        editorial VARCHAR(50),
                        genero VARCHAR(50),
                        categoria VARCHAR(50),
                        tematica VARCHAR(50),
                        CONSTRAINT pk_libro PRIMARY KEY (isbn, id),
                        CONSTRAINT fk_libro_id FOREIGN KEY (id) REFERENCES documento(id),
                        CONSTRAINT fk_libro_genero FOREIGN KEY (genero) REFERENCES genero(nombre),
                        CONSTRAINT fk_libro_categoria FOREIGN KEY (categoria) REFERENCES categoria(nombre)
                    );
            """
            #cursor.execute(create_table_libro)
            #con.commit()

            create_table_otro = f"""
                    CREATE TABLE IF NOT EXISTS db_librerio.otro(
                        id INT PRIMARY KEY,
                        emisor VARCHAR(50),
                        tipo VARCHAR(50) NOT NULL, 
                        subtipo VARCHAR(50) NOT NULL,
                        CONSTRAINT fk_otro_id FOREIGN KEY (id) REFERENCES documento(id)
                    );
            """
            #cursor.execute(create_table_otro)
            #con.commit()

            print("Tablas creadas con éxito")
            #sql = "INSERT INTO usuarios VALUES(null,%s,%s,%s);"
            #con.commit()
            #print(cursor.rowcount, "Registro ingresado")
        except mysql.connector.Error as error:
            print(f'Error: {error}')
        
        finally:
            pass 
            #cursor.close()
            #con.close()

