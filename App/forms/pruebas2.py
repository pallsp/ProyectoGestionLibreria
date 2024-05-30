"""import os
import tkinter as tk
from tkinter import Listbox, Scrollbar, Button, Label, messagebox

class CustomFileDialog(tk.Toplevel):
    def __init__(self, parent, initialdir='/', filetypes=[('PDF files', '*.pdf')], *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.initialdir = initialdir
        self.filetypes = filetypes
        self.selected_file = None
        
        self.title("Select a PDF file")
        self.geometry("600x400")

        self.current_path = initialdir
        self.create_widgets()
        self.list_directory(initialdir)
        
    def create_widgets(self):
        self.dir_label = Label(self, text=self.current_path)
        self.dir_label.pack(pady=5)
        
        self.listbox = Listbox(self, selectmode=tk.SINGLE, width=80, height=20)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = Scrollbar(self, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.select_button = Button(self, text="Select", command=self.select_file)
        self.select_button.pack(side=tk.BOTTOM, pady=5)
        
        self.listbox.bind('<Double-1>', self.on_double_click)

    def list_directory(self, path):
        self.listbox.delete(0, tk.END)
        self.dir_label.config(text=path)
        self.current_path = path
        
        try:
            items = os.listdir(path)
            items = sorted(item for item in items if not item.startswith('.'))
            for item in items:
                self.listbox.insert(tk.END, item)
        except PermissionError:
            messagebox.showerror("Error", "You do not have permission to access this folder.")
        
    def on_double_click(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            value = self.listbox.get(index)
            full_path = os.path.join(self.current_path, value)
            
            if os.path.isdir(full_path):
                self.list_directory(full_path)
            elif full_path.lower().endswith('.pdf'):
                self.selected_file = full_path
                self.destroy()
    
    def select_file(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            value = self.listbox.get(index)
            full_path = os.path.join(self.current_path, value)
            
            if os.path.isdir(full_path):
                self.list_directory(full_path)
            elif full_path.lower().endswith('.pdf'):
                self.selected_file = full_path
                self.destroy()
    
    def show(self):
        self.wait_window()
        return self.selected_file

def open_custom_dialog():
    dialog = CustomFileDialog(root, initialdir=os.path.expanduser('~'), filetypes=[('PDF files', '*.pdf')])
    selected_file = dialog.show()
    if selected_file:
        print(f"Selected file: {selected_file}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("200x100")
    open_button = Button(root, text="Open Custom File Dialog", command=open_custom_dialog)
    open_button.pack(pady=20)
    root.mainloop()
"""

"""import os
import tkinter as tk
from tkinter import Button, Label, messagebox, Toplevel
from tkinter import ttk

class CustomFileDialog(Toplevel):
    def __init__(self, parent, initialdir='/', filetypes=[('PDF files', '*.pdf')], *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.initialdir = initialdir
        self.filetypes = filetypes
        self.selected_file = None
        
        self.title("Select a PDF file")
        self.geometry("800x600")
        self.config(bg="#2e2e2e")

        self.current_path = initialdir
        self.create_widgets()
        self.list_directory(initialdir)
        
    def create_widgets(self):
        self.dir_label = Label(self, text=self.current_path, bg="#2e2e2e", fg="#ffffff")
        self.dir_label.pack(pady=5)
        
        self.canvas = tk.Canvas(self, bg="#2e2e2e")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.frame = tk.Frame(self.canvas, bg="#2e2e2e")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.select_button = Button(self, text="Select", command=self.select_file, bg="#4CAF50", fg="#ffffff")
        self.select_button.pack(side=tk.BOTTOM, pady=5)
        
    def list_directory(self, path):
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        self.dir_label.config(text=path)
        self.current_path = path
        
        try:
            items = os.listdir(path)
            items = sorted(item for item in items if not item.startswith('.'))
            row, col = 0, 0
            for item in items:
                full_path = os.path.join(self.current_path, item)
                if os.path.isdir(full_path):
                    item_label = Label(self.frame, text=item, bg="#3e3e3e", fg="#ffffff", width=20, height=2, relief="groove")
                elif item.lower().endswith('.pdf'):
                    item_label = Label(self.frame, text=item, bg="#616161", fg="#ffffff", width=20, height=2, relief="groove")
                else:
                    continue
                
                item_label.grid(row=row, column=col, padx=5, pady=5)
                item_label.bind("<Double-1>", lambda e, path=full_path: self.on_double_click(path))
                col += 1
                if col >= 6:
                    col = 0
                    row += 1
        except PermissionError:
            messagebox.showerror("Error", "You do not have permission to access this folder.")
        
    def on_double_click(self, full_path):
        if os.path.isdir(full_path):
            self.list_directory(full_path)
        elif full_path.lower().endswith('.pdf'):
            self.selected_file = full_path
            self.destroy()
    
    def select_file(self):
        selected_item = self.frame.focus_get()
        if selected_item:
            full_path = selected_item.cget("text")
            full_path = os.path.join(self.current_path, full_path)
            if os.path.isdir(full_path):
                self.list_directory(full_path)
            elif full_path.lower().endswith('.pdf'):
                self.selected_file = full_path
                self.destroy()
    
    def show(self):
        self.wait_window()
        return self.selected_file

def open_custom_dialog():
    dialog = CustomFileDialog(root, initialdir=os.path.expanduser('~'), filetypes=[('PDF files', '*.pdf')])
    selected_file = dialog.show()
    if selected_file:
        print(f"Selected file: {selected_file}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("200x100")
    open_button = Button(root, text="Open Custom File Dialog", command=open_custom_dialog)
    open_button.pack(pady=20)
    root.mainloop()"""
    
    
"""import tkinter as tk
from tkinter import font
from ttkbootstrap import Style

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Font Awesome Example")
        self.geometry("1500x300")

        # Asegúrate de que Font Awesome esté disponible
        font_awesome = font.Font(family='FontAwesome', size=12)
        
        # Verifica si Font Awesome está en las fuentes disponibles
        if 'FontAwesome' not in font.families():
            print("FontAwesome no está disponible. Asegúrate de que la fuente esté instalada en tu sistema.")

        # Crear un botón usando Font Awesome para el icono de barras de menú
        self.btnocultar = tk.Button(self, text="\uf0c9", font=font_awesome, command=self.toggle_menu_lateral, bd=0, bg="#df5553", fg="white")
        self.btnocultar.place(x=210, y=40)

        # Crear botones adicionales para probar otros caracteres Unicode
        self.btninfo = tk.Button(self, text="\u24D8", font=font_awesome, command=self.open_info, bd=0, bg="#df5553", fg="white")
        self.btninfo.place(x=1420, y=5, width=30, height=30)

        self.btnlicense = tk.Button(self, text=u"\U0001F12F", font=font_awesome, command=self.open_license, bd=0, bg="#df5553", fg="white")
        self.btnlicense.place(x=1460, y=5, width=30, height=30)

        # Otro botón para probar otro icono de Font Awesome
        self.btnanother = tk.Button(self, text="\uf0a1", font=font_awesome, command=self.another_action, bd=0, bg="#df5553", fg="white")  # Icono de fa-bullhorn
        self.btnanother.place(x=50, y=100)

    def toggle_menu_lateral(self):
        # Lógica para el menú lateral
        print("Menú lateral ocultado/mostrado")

    def open_info(self):
        # Lógica para abrir información
        print("Información abierta")

    def open_license(self):
        # Lógica para abrir licencia
        print("Licencia abierta")

    def another_action(self):
        # Lógica para otra acción
        print("Otra acción")

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()"""
    
# --------------------- CORREO ---------------------------
"""import os 
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import ssl
from datetime import datetime
from tkinter import messagebox
    
try:
    load_dotenv()
    password = os.getenv("PASSWORD")
    email_sender = "libreriocontacto@gmail.com"
    email_receiver = "miguelo808@gmail.com"
    subject = "Confirmación de registro"
    body = "Bienvenido a la comunidad de Librerio, Pablo!!! Esperamos que puedas disfrutar de la aplicación"

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
    #messagebox.showerror(message = "Ha ocurrido un error inesperado, por favor ingrese el correo más tarde", title = "Error", parent=self.ventana)"""

"""from random import *

def generateCode():
    letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numero = randint(0, 10000)
    letra = choice(letras)
    print(f"{letra}{numero}")"""
    
numeros = [0,1,2,3,4,5,6,7]
    
for n in numeros: 
    print((n%3)+1)

