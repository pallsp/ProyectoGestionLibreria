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

#------------ LÓGICA INICIO DE SESIÓN-----------------
#heredará de la clase de diseño
class FormLogin(FormLoginDesigner):

    def __init__(self):
        self.database_manager = DatabaseManager()
        super().__init__()

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
