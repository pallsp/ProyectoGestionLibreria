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
from datetime import datetime
from tkinter import messagebox

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
            usuario.foto = "/home/pablo/PROYECTO/imagenes/libreriologo.png" # foto por defecto HAY QUE CAMBIAR LA RUTA
            nombre_u = usuario.nombre
            correo_u = usuario.correo
            if usuario.nombre == "" or usuario.password == "" or usuario.correo == "": # si falta algún campo
                messagebox.showerror(message = "Faltan campos, por favor rellena todos los campos.", title = "Mensaje", parent=self.ventana)
            #self.database_manager = DatabaseManager(usuario.nombre, usuario.password, db_usuario)
            elif not(self.isUserRegister(usuario)): # si el usuario no estaba registrado anteriormente
                usuario.password = self.do_hash(self.passw.get()) #cript_dec.encrypted(self.passw.get())
                usuario.cuenta = Cuenta(fecha_creacion=datetime.now().date()) # creamos la cuenta asociada al usuario
                usuario.biblioteca = Biblioteca(id=f"bib-{self.usuario.get()}", fecha_creacion=datetime.now().date()) # creamos la biblioteca asociada al usuario  
                self.database_manager.insertUser(usuario) # insertamos usuario en la tabla de usuarios registrados y creamos el usuario en la base de datos
                messagebox.showinfo(message = f"Usuario registrado correctamente con correo {self.email.get()}.", title = "Mensaje", parent=self.ventana)
                #self.create_user_things(self.usuario.get())
                self.ventana.destroy()
                self.send_correo(correo_u, nombre_u) # enviar correo confirmación

    def do_hash(self, texto: str):
        hasher = hashlib.sha3_512()
        hasher.update(texto.encode('utf-8'))
        return hasher.hexdigest() 

    def isConfirmationPassword(self):
        status: bool = True
        if self.passw.get() != self.passw_conf.get():
            status = False
            messagebox.showerror(message = "Las contraseñas no coinciden, revisa el registro.", title = "Error", parent=self.ventana)
            self.passw.delete(0, tk.END)
            self.passw_conf.delete(0, tk.END)
        return status
        
    def isUserRegister(self, user: Usuario):
        status: bool = False
        usuarios_registrados = self.database_manager.getUsers()
        for usu in usuarios_registrados: 
            if user.id == usu.id:
                status = True
                messagebox.showerror(message = "Usuario ya registrado.", title = "Error")
        return status

    def send_correo(self, correo, nombre):
        try:
            load_dotenv()
            password = os.getenv("PASSWORD")
            email_sender = "libreriocontacto@gmail.com"
            email_receiver = correo
            subject = "Confirmación de registro"
            body = f"Bienvenido a la comunidad de Librerio, {nombre}!!! Esperamos que puedas disfrutar de la aplicación"
            em = EmailMessage()
            em["From"] = email_sender
            em["To"] = email_receiver
            em["Subject"] = subject
            em.set_content(body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context = context) as smtp:
                smtp.login(email_sender, password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
        except smtplib.SMTPException as e:
            print(f"Error inesperado al enviar el correo: {e}")
            messagebox.showerror(message = "Ha ocurrido un error inesperado, por favor ingrese el correo más tarde", title = "Error", parent=self.ventana)

    def create_user_things(self, nombre_usuario, id_usuario):
        fecha_actual = datetime.now().date()
        self.database_manager.createBiblioteca(f"bib-{nombre_usuario}", id_usuario, fecha_actual) # creamos la biblioteca


