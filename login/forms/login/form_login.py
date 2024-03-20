import tkinter as tk 
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.generic as utl
from forms.master.form_master import MasterPanel
from forms.login.form_login_designer import FormLoginDesigner

#heredará de la clase de diseño
class FormLogin(FormLoginDesigner):

    def check_session(self): #verificar el usuario y la contraseña
        usr = self.usuario.get() #.get() para obtener los valores de los campos de texto/entrada
        password = self.passw.get()
        if usr == "root" and password == "1234":
            self.ventana.destroy()
            #esperar a entrar
            MasterPanel()
        else:
            messagebox.showerror(message = "La contraseña no es correcta", title = "Error")

    def __init__(self):
        super().__init__()
