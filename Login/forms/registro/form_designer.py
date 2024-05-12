import tkinter as tk 
from tkinter import ttk
from tkinter.font import BOLD
import util.generic as utl
from forms.master.form_master import MasterPanel

# ------------------------------- DISEÑO REGISTRO----------------------------
#clase para el diseño
class FormRegisterDesigner:
    def register():
        pass
    
    def __init__(self):
        self.ventana = tk.Toplevel() #genera formulario con referencia al anterior
        self.ventana.title("Registro de usuario")
        self.ventana.config(bg = "#fcfcfc")
        self.ventana.resizable(width = 0, height = 0)
        utl.centrar_ventana(self.ventana, 650, 520) #razón 1.25

        logo = utl.leer_imagen("/home/pablo/PROYECTO/Login/imagenes/libreriologo.png", (200,200))

        #frame_logo #F87474
        frame_logo = tk.Frame(self.ventana, bd = 0, width = 200, relief = tk.SOLID, padx = 10, pady = 10, bg = "#df5553")
        frame_logo.pack(side = "left", expand = tk.NO, fill = tk.BOTH)
        label = tk.Label(frame_logo, image = logo, bg = "#df5553")
        label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        #frame_form
        frame_form = tk.Frame(self.ventana, bd = 0, relief = tk.SOLID, bg = "#fcfcfc")
        frame_form.pack(side = "right", expand = tk.YES, fill = tk.BOTH)

        #frame_form_top
        frame_form_top = tk.Frame(frame_form, height = 50, bd = 0, relief = tk.SOLID, bg = "black")
        frame_form_top.pack(side = "top", fill = tk.X)
        title = tk.Label(frame_form_top, text = "Registro de usuario", font = ("Times", 30), fg = "#666a88", bg = "#fcfcfc", pady = 50)
        title.pack(expand = tk.YES, fill = tk.BOTH)

        #frame_form_fill
        frame_form_fill = tk.Frame(frame_form, height = 50, bd = 0, relief = tk.SOLID, bg = "#fcfcfc")
        frame_form_fill.pack(side = "bottom", expand = tk.YES, fill = tk.BOTH)

        #etiqueta correo y campo de entrada
        lbl_correo = tk.Label(frame_form_fill, text="Correo", font=("Times", 14), fg = "#666a88", bg = "#fcfcfc", anchor ="w")
        lbl_correo.pack(fill=tk.X, padx = 20, pady = 5)
        self.email = ttk.Entry(frame_form_fill, font = ("Times", 14))
        self.email.pack(fill = tk.X, padx = 20, pady = 10)

        #etiqueta usuario y campo de entrada
        lbl_usuario = tk.Label(frame_form_fill, text = "Usuario", font = ("Times", 14), fg = "#666a88", bg = "#fcfcfc", anchor = "w")
        lbl_usuario.pack(fill = tk.X, padx = 20, pady = 5)
        self.usuario = ttk.Entry(frame_form_fill, font = ("Times", 14))
        self.usuario.pack(fill = tk.X, padx = 20, pady = 10)

        #etiqueta contraseña y campo de entrada
        lbl_passw = tk.Label(frame_form_fill, text = "Contraseña", font = ("Times", 14), fg = "#666a88", bg = "#fcfcfc", anchor = "w")
        lbl_passw.pack(fill = tk.X, padx = 20, pady = 5)
        self.passw = ttk.Entry(frame_form_fill, font = ("Times", 14))
        self.passw.pack(fill = tk.X, padx = 20, pady = 10)
        self.passw.config(show = "*") #para mostrar * en lugar de lo que escribimos

        #etiqueta confirmación contraseña y campo de entrada
        lbl_passw_conf = tk.Label(frame_form_fill, text = "Confirmación", font = ("Times", 14), fg = "#666a88", bg = "#fcfcfc", anchor = "w")
        lbl_passw_conf.pack(fill = tk.X, padx = 20, pady = 5)
        self.passw_conf = ttk.Entry(frame_form_fill, font = ("Times", 14))
        self.passw_conf.pack(fill = tk.X, padx = 20, pady = 10)
        self.passw_conf.config(show = "*")

        #boton registrar #F87474
        registro = tk.Button(frame_form_fill, text = "Registrar", font = ("Times", 15, BOLD), bg = "#df5553", bd = 0, fg = "#fcfcfc", command = self.register) 
        registro.pack(fill = tk.X, padx = 20, pady = 20)
        registro.bind("<Return>", (lambda event: self.register())) 
        
        self.ventana.mainloop()