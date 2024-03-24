from forms.registro.form_designer import FormRegisterDesigner
from persistence.repository.auth_user_repository import AuthUserRepository
from persistence.model import Auth_User
from tkinter import messagebox
import util.cript_decript as cript_dec
import tkinter as tk


class FormRegister(FormRegisterDesigner):
    def __init__(self):
        self.auth_repository = AuthUserRepository()
        super().__init__()
    
    def register(self):
        if self.isConfirmationPassword():
            user = Auth_User()
            user.username = self.usuario.get()
            user_db: Auth_User = self.auth_repository.getUserByUserName(self.usuario.get())
            if not(self.isUserRegister(user_db)):
                user.password = cript_dec.encrypted(self.passw.get())
                self.auth_repository.insertUser(user)
                messagebox.showinfo(message = "Usuario registrado correctamente", title = "Mensaje")
                self.ventana.destroy()

    def isConfirmationPassword(self):
        status: bool = True
        if self.passw.get() != self.passw_conf.get():
            status = False
            messagebox.showerror(message = "Las contraseñas no coinciden, revisa el registro", title = "Mensaje")
            self.passw.delete(0, tk.END)
            self.passw_conf.delete(0, tk.END)
        return status
        
    def isUserRegister(self, user: Auth_User):
        status: bool = False
        if user != None:
            status = True
            messagebox.showerror(message = "El usuario ya existe", title = "Mensaje")
        return status
