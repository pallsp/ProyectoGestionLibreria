import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import re

import os 
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import ssl
"""class Window(tk.Tk):
    def __init__(self, theme_name='superhero', title="Cambiar Tema", width=300, height=200, resizable=(False, False)):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(*resizable)

        self.estilo = Style(theme=theme_name)

        self.boton_cambiar_tema = ttk.Checkbutton(self, text="Cambiar Tema", command=self.cambiar_tema, bootstyle="dark-round-toggle")
        self.boton_cambiar_tema.pack(pady=20)

        self.tema_actual = theme_name

    def cambiar_tema(self):
        # Cambiar el tema entre 'superhero' y 'darkly'
        self.tema_actual = 'darkly' if self.tema_actual == 'superhero' else 'superhero'
        self.estilo.theme_use(self.tema_actual)

# Crear la instancia de la ventana
ventana = Window()

# Ejecutar la ventana
ventana.mainloop()"""

"""patron_fecha = r'^\d{4}-\d{2}-\d{2}$'
fecha = input("Introduce una fecha: ")
if re.match(patron_fecha, fecha):
    print("fecha en el formato adecuado")
else: 
    print("fecha incorrecta")"""
"""nombre = "pablo"
load_dotenv()
password = os.getenv("PASSWORD")
email_sender = "libreriocontacto@gmail.com"
email_receiver = "pallsp00@gmail.com"
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
    smtp.sendmail(email_sender, email_receiver, em.as_string())"""

cadena: str = input("Introduce una cadena de dígitos: ")
if cadena.isdigit():
    print("son digitos")
else:
    print("no son digitos")
