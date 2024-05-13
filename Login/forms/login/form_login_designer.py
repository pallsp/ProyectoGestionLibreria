import tkinter as tk 
from tkinter import ttk
from tkinter.font import BOLD
import util.generic as utl
from forms.master.form_master import MasterPanel
#from ttkbootstrap import * 

# --------------------- DISEÑO INICIO DE SESIÓN-----------------------
#clase para el diseño
class FormLoginDesigner:
    def check_session(self): #verificar el usuario y la contraseña
        pass
    
    def register_user(self): #registrar usuario
        pass

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Inicio de sesión")
        self.ventana.geometry("800x500")
        self.ventana.config(bg = "#fcfcfc") #fcfcfc #df5553
        self.ventana.resizable(width = 0, height = 0)
        utl.centrar_ventana(self.ventana, 800, 500)

        logo = utl.leer_imagen("/home/pablo/PROYECTO/Login/imagenes/libreriologo.png", (200,200))

        #frame_logo   ESTE UNO
        frame_logo = tk.Frame(self.ventana, bd = 0, width = 300, relief = tk.SOLID, padx = 10, pady = 10, bg = "#df5553") #3a7ff6 ESTE UNO bg = "#df5553"
        frame_logo.pack(side = "left", expand = tk.NO, fill = tk.BOTH)
        label = tk.Label(frame_logo, image = logo, bg = "#df5553") #3a7ff6 ESTE OTRO bg = "#df5553"
        label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        #frame_form
        frame_form = tk.Frame(self.ventana, bd = 0, relief = tk.SOLID, bg = "#fcfcfc")
        frame_form.pack(side = "right", expand = tk.YES, fill = tk.BOTH)

        #frame_form_top
        frame_form_top = tk.Frame(frame_form, height = 50, bd = 0, relief = tk.SOLID, background = "black")
        frame_form_top.pack(side = "top", fill = tk.X)
        title = tk.Label(frame_form_top, text = "Inicio de sesión", font = ("Times", 30), foreground = "#666a88", background = "#fcfcfc", pady = 50) #666a88
        title.pack(expand = tk.YES, fill = tk.BOTH)

        #frame_form_fill
        frame_form_fill = tk.Frame(frame_form, height = 50, bd = 0, relief = tk.SOLID, background = "#fcfcfc")
        frame_form_fill.pack(side = "bottom", expand = tk.YES, fill = tk.BOTH)

        #etiqueta usuario y campo de entrada
        lbl_usuario = tk.Label(frame_form_fill, text = "Usuario", font = ("Times", 14), foreground = "#666a88", background = "#fcfcfc", anchor = "w")
        lbl_usuario.pack(fill = tk.X, padx = 20, pady = 5)
        self.usuario = ttk.Entry(frame_form_fill, font = ("Times", 14))
        self.usuario.pack(fill = tk.X, padx = 20, pady = 10)

        #etiqueta contraseña y campo de entrada
        lbl_passw = tk.Label(frame_form_fill, text = "Contraseña", font = ("Times", 14), foreground = "#666a88", background = "#fcfcfc", anchor = "w")
        lbl_passw.pack(fill = tk.X, padx = 20, pady = 5)
        self.passw = ttk.Entry(frame_form_fill, font = ("Times", 14))
        self.passw.pack(fill = tk.X, padx = 20, pady = 10)
        self.passw.config(show = "*") #para mostrar * en lugar de lo que escribimos

        #boton inicio de sesion #3a7ff6
        inicio = tk.Button(frame_form_fill, text = "Iniciar sesión", font = ("Times", 15, BOLD), background = "#df5553", bd = 0, foreground = "#fff", command = self.check_session) #command = self.check_session la función que se ejecutará
        inicio.pack(fill = tk.X, padx = 20, pady = 20)
        #inicio.bind("<Return>", (lambda event: self.check_session())) usamos bind para lanzar un evento, en este caso usando una función lambda

        #boton registro usuario #fcfcfc #3a7ff6
        registro = tk.Button(frame_form_fill, text = "Registrar usuario", font = ("Times", 15, BOLD), background = "#fcfcfc", bd = 0, foreground = "#df5553", command = self.register_user) 
        registro.pack(fill = tk.X, padx = 20, pady = 20)

        self.ventana.mainloop()
