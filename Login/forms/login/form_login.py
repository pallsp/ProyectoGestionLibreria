import tkinter as tk 
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.generic as utl
from forms.master.form_master import MasterPanel
from forms.login.form_login_designer import FormLoginDesigner
from persistence.repository.database_manager import DatabaseManager
from persistence.model import *
import util.cript_decript as cript_dec
from forms.registro.form_register import FormRegister
import hashlib 
from random import *
import os 
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import ssl
from datetime import datetime
from tkinter import messagebox

#------------ LÓGICA INICIO DE SESIÓN-----------------
#heredará de la clase de diseño
class FormLogin(FormLoginDesigner):

    def __init__(self):
        self.database_manager = DatabaseManager()
        super().__init__()
        self.set_icon()
    
    def set_icon(self):
        self.iconphoto(False, tk.PhotoImage(file="/home/pablo/PROYECTO/imagenes/libreriologo.png"))

    def check_session(self): #verificar el usuario y la contraseña
        #user_db: Usuario = self.database_manager.getUserByUserName(self.usuario.get())
        #user_db: Usuario  
        nombre = self.usuario.get() # obtengo el nombre del usuario
        #password = self.passw.get() # obtengo la contraseña del usuario
        user = self.isUser(nombre)
        if(user == None): # si no es un usuario registrado
            messagebox.showerror(message = "El usuario no existe por favor registrese", title = "Mensaje")
            self.limpiar()
        else: # si es un usuario registrado
            self.isPassword(self.passw.get(), user) # si es su contraseña 

    def limpiar(self):
        self.usuario.delete(0, tk.END)
        self.passw.delete(0, tk.END)

    def register_user(self):
        FormRegister().mainloop()

    def isUser(self, nombre):
        return self.database_manager.getUserByUserName(nombre)
        if user == None:
            status = False
            messagebox.showerror(message = "El usuario no existe por favor registrese", title = "Mensaje")
        return status
    
    def isPassword(self, password: str, user: Usuario):
        hash_password = self.do_hash(password) #cript_dec.decrypt(user.password)
        if hash_password == user.password:
            self.ventana.destroy()
            # ejecutar la aplicación pasandole el user.id
            #MasterPanel()
            print(user.id) # devuelvo el id

        else:
            messagebox.showerror(message = "La contraseña no es correcta", title = "Mensaje")

    def do_hash(self, texto: str):
        hasher = hashlib.sha3_512()
        hasher.update(texto.encode('utf-8'))
        return hasher.hexdigest() 
    
    # ------------------------------- LÓGICA RECUPERAR CONTRASEÑA ----------------------------------------
    # GENERAR CÓDIGO RECUPERACIÓN
    def generateCode(self):
        letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numero = randint(0, 10000)
        letra = choice(letras)
        return f"{letra}{numero}"
    
    # ENVIAR CODIGO RECUPERACION 
    def sendRecoverEmail(self, code, correo):
        try:
            load_dotenv()
            password = os.getenv("PASSWORD")
            email_sender = "libreriocontacto@gmail.com"
            email_receiver = correo
            subject = "Recuperación contraseña"
            body = f"Tu código de recuperación de contraseña es: {code}. Introdúcelo para poder cambiar a una nueva contraseña."

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
            
    # RECUPERAR CONTRASEÑA
    def recuperar_passw(self):
        #messagebox.showerror(message = "Intro", title = "Error", parent=self.ventana)
        self.popup = tk.Toplevel(self.ventana)
        self.popup.geometry("400x200")
        self.popup.resizable(False, False)
        ttk.Label(self.popup, text="Introduce el usuario de la cuenta a recuperar:").place(x=30, y=20)
        self.user_entry = ttk.Entry(self.popup, width=30)
        self.user_entry.place(x=80, y=65)
        self.user_entry.focus_set()
        ttk.Button(self.popup, text="Confirmar", command=lambda: self.check_user(self.user_entry.get())).place(x=300, y=160)

    # COMPROBAR CORREO
    def check_user(self, usuario):
        try:
            if usuario in self.database_manager.selectAllUserNames():
                correo = self.database_manager.selectCorreoByName(self.user_entry.get())
                messagebox.showinfo(title="Éxito", message=f"Usuario registrado, se enviará un código de confirmación a su correo", parent=self.popup)
                codigo = self.generateCode()
                self.sendRecoverEmail(codigo, correo)
                self.popup.destroy()
                self.ask_code(codigo, usuario) 
        except Exception as e: 
            messagebox.showerror(title="Error", message="Usuario no registrado. Pruebe de nuevo", alert=True, parent=self.popup)
            self.popup.destroy()
        """else:
            messagebox.showerror(title="Error", message="Usuario no registrado. Pruebe de nuevo", alert=True, parent=self.popup)
            self.popup.destroy()"""
            
    # PEDIR CÓDIGO
    def ask_code(self, codigo, usuario):
        self.popup = tk.Toplevel(self.ventana)
        self.popup.geometry("400x200")
        self.popup.resizable(False, False)
        ttk.Label(self.popup, text="Introduce el código enviado:").place(x=30,y=20)
        self.code_entry = ttk.Entry(self.popup, width=30)
        self.code_entry.place(x=80,y=65)
        self.code_entry.focus_set()
        ttk.Button(self.popup, text="Confirmar", command=lambda: self.check_code(codigo, self.code_entry.get(), usuario)).place(x=300,y=160)
    
    # COMPROBAR CÓDIGO
    def check_code(self, codigo, codigo_introducido, usuario):
        if codigo == codigo_introducido:
            messagebox.showinfo(title="Éxito", message="Código correcto. Puedes cambiar la contraseña.", parent=self.popup)
            self.popup.destroy()
            self.change_passw(usuario)
        else:
            messagebox.showerror(title="Error", message="Código incorrecto. Pruebe otra vez.", alert=True, parent=self.popup)
            self.popup.destroy()
    
    # CAMBIAR CONTRASEÑA
    def change_passw(self, usuario):
        self.popup = tk.Toplevel(self.ventana)
        self.popup.geometry("500x250")
        self.popup.resizable(False, False)
        self.popup.config(bg = "#df5553") #fcfcfc #df5553
        ttk.Label(self.popup, text="Introduce la nueva contraseña:", font = ("Times", 14), foreground = "#403d3c", background = "#df5553", anchor = "w").place(x=30, y=20)
        self.passw_entry = ttk.Entry(self.popup, show="*", width=30)
        self.passw_entry.place(x=80, y=65)
        self.passw_entry.focus_set()
        ttk.Label(self.popup, text="Introduce la nueva contraseña:", font = ("Times", 14), foreground = "#403d3c", background = "#df5553", anchor = "w").place(x=30, y=90)
        self.passw_conf_entry = ttk.Entry(self.popup, show="*", width=30)
        self.passw_conf_entry.place(x=80, y=135)
        self.passw_conf_entry.focus_set()
        ttk.Button(self.popup, text="Confirmar", command=lambda: self.check_change_passw(self.passw_entry.get(), self.passw_conf_entry.get(), usuario)).place(x=400, y=190)
    
    # COMPROBAR CONTRASEÑA
    def check_change_passw(self, passw, passwconf, usuario):
        if passw == passwconf:
            self.database_manager.updatePasswordUser(usuario, self.do_hash(passw))
            messagebox.showinfo(title="Éxito", message="Contraseña cambiada con éxito.", parent=self.popup)
            self.popup.destroy()
        else:
            messagebox.showerror(title="Error", message="Las contraseñas no coinciden. Deben coincidir.", alert=True, parent=self.popup)
            self.passw_entry.delete(0, tk.END)
            self.passw_conf_entry.delete(0, tk.END)
