import tkinter as tk 
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import util.generic as utl
from forms.master.form_master import MasterPanel
from forms.login.form_login_designer import FormLoginDesigner
from persistence.repository.auth_user_repository import AuthUserRepository
from persistence.model import Auth_User
import util.cript_decript as cript_dec
from forms.registro.form_register import FormRegister

#heredará de la clase de diseño
class FormLogin(FormLoginDesigner):

    def __init__(self):
        self.auth_repository = AuthUserRepository()
        super().__init__()

    def check_session(self): #verificar el usuario y la contraseña
        user_db: Auth_User = self.auth_repository.getUserByUserName(self.usuario.get())
        if(self.isUser(user_db)):
            self.isPassword(self.passw.get(), user_db)

    def register_user(self):
        FormRegister().mainloop()

    def isUser(self, user: Auth_User):
        status: bool = True
        if user == None:
            status = False
            messagebox.showerror(message = "El usuario no existe por favor registrese", title = "Mensaje")
        return status
    
    def isPassword(self, password: str, user: Auth_User):
        b_password = cript_dec.decrypt(user.password)
        if password == b_password:
            self.ventana.destroy()
            MasterPanel()
        else:
            messagebox.showerror(message = "La contraseña no es correcta", title = "Mensaje")

