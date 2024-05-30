from ttkbootstrap import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from persistence.repository.database_manager import DatabaseManager
from persistence.model import *
import image_handler as img
import hashlib
import util.generic as utl_img 
import re 

from ttkbootstrap import * 
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox

class Ajustes(Frame):
    def __init__(self, id, padre, master = None):
        super().__init__(master)
        self.database_manager = DatabaseManager() # establecer el gestor de la base de datos
        self.user_id = id
        self.user: Usuario = self.database_manager.selectUserById(self.user_id)
        self.elegir_foto = False
        #super().__init__(themename="superhero", size=(1260, 700), title="Interfaz moderna") #proporcion 1.8
        self.principal:LabelFrame = master
        self.padre_principal = padre
        self.image_path = self.user.foto
        self.set_image_perfil(self.image_path) # establecer la foto de perfil
        self.widgets() # establecer los widgets de la pantalla

    # MÉTODOS IMAGEN PERFIL
    def set_image_perfil(self, path): #"/home/pablo/Escritorio/ProyectoFinalDAM/LibreriaGestion/login/sidebar_menu/imagenes/Perfil.jpeg"
        if path is not None:
            self.perfil = utl_img.leer_imagen(path, (70, 70))
        else: 
            self.perfil = utl_img.leer_imagen("/home/pablo/Escritorio/ProyectoFinalDAM/LibreriaGestion/login/sidebar_menu/imagenes/Perfil.jpeg", (70, 70))

    def set_image_frame(self):
        self.lblimageperfil = Frame(self.principal, bootstyle = INFO)
        self.lblimageperfil.place(x=920, y=190, width=70, height=70)

        self.labelPerfil = Label(self.lblimageperfil, image=self.perfil)
        self.labelPerfil.pack(side=tk.TOP, fill=BOTH, expand=True)

    def open_file_dialog(self):
        self.elegir_foto = True
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            print("Archivo seleccionado: ", self.image_path)
            self.set_image_perfil(self.image_path)
            self.set_image_frame()

    # MÉTODOS WIDGETS
    def entry_label(self,frame,x,y,texto):
        lbl = Label(frame, text=texto,bootstyle=PRIMARY)
        lbl.place(x=x,y=y)

        if texto == "Nueva contraseña" or texto == "Confirmar nueva contraseña":
            entry = Entry(frame, bootstyle=(PRIMARY), show="*")
            entry.place(x=x+210,y=y)
        else:
            entry = Entry(frame, bootstyle=(PRIMARY))
            entry.place(x=x+210,y=y)
        return entry

    def comboboxea(self, frame, x, y, texto, opciones):
        lbl = Label(frame, text=texto,bootstyle=PRIMARY)
        lbl.place(x=x,y=y)

        combo = Combobox(frame, values=opciones)
        combo.current(0)
        combo.place(x=x+100,y=y)
        return combo
    
    # EDITAR (NECESARIO PULSAR PARA PODER GUARDAR O DESCARTAR)
    def editar(self):
        self.btnguardar.configure(state="active")
        self.btndescartar.configure(state="active")
        self.btnfotoperfil.configure(state="active")
       
    # ELIMINAR CUENTA 
    def eliminar_cuenta(self):
        self.ask_for_passw("Introduce la contraseña para continuar: ", "eliminar")
    
    # GUARDAR CAMBIOS
    def guardar_cambios(self):
        if self.validar(): # validar los campos
            self.ask_for_passw("Introduce la contraseña para confirmar los cambios: ", "guardar")
    
    # DESCARTAR CAMBIOS
    def descartar(self):
        self.limpiar()
        self.btnguardar.configure(state="disabled")
        self.btndescartar.configure(state="disabled")
        self.elegir_foto = False
    
    # LIMPIAR CAMPOS
    def limpiar(self):
        self.e_newusuario.delete(0, END)
        self.e_newpassw.delete(0, END)
        self.e_newpasswconf.delete(0, END)
        self.e_newcorreoe.delete(0, END)
        self.e_newlocalidad.delete(0, END)
        self.e_newnacimiento.delete(0, END)
    
    # VALIDAR  FECHA YYYY-MM-DD
    def validar(self):
        patron_fecha = r'^\d{4}-\d{2}-\d{2}$'
        if self.e_newusuario.get() == "" and self.e_newpassw.get() == "" and self.e_newpasswconf.get() == "" and self.e_newcorreoe.get() == "" and self.e_newlocalidad.get() == "" and self.e_nacimiento.get() == "" and not self.elegir_foto:
            Messagebox.show_error(title="Error", message="Están todos los campos vacíos", alert=True)
            return False
        elif self.e_newpassw.get() != self.e_newpasswconf.get():
            Messagebox.show_error(title="Error",message="Las contraseñas no coinciden", alert=True)
            return False
        elif not re.match(patron_fecha, self.e_newnacimiento.get()):
            Messagebox.show_error(title="Error", message="La fecha no está en el formato adecuado", alert=True)
            return False
        return True
    
    # MÉTODOS LLAMADOS
    def guardar(self):
        nombre = self.e_newusuario.get()
        passw = self.e_newpassw.get()
        correo = self.e_newcorreoe.get()
        localidad = self.e_newlocalidad.get()
        nacimiento = self.e_newnacimiento.get()
        image = self.image_path
        if nombre == "":
            nombre = self.user.nombre
        if passw == "":
            passw = self.user.password
        else:
            passw = self.do_hash(self.e_newpassw.get())
        if correo == "":
            correo = self.user.correo
        if image == "":
            image = self.user.foto
        self.database_manager.updateUsuario(self.user_id, nombre, passw, correo, localidad, nacimiento, image)
        self.limpiar()
        Messagebox.show_info(title="Éxito", message="Cambios guardados con éxito. Para que se apliquen necesitas reiniciar la aplicación", parent=self)
        
    
    def eliminar(self):
        valor = Messagebox.show_question(title="Alertar", message="¿Estás seguro de que deseas eliminar tu cuenta?", alert=True, parent=self)
        if valor == "Sí":
            self.database_manager.deleteCuenta(self.user_id)
            self.principal.destroy()
            self.padre_principal.destroy()
    
    def widgets(self):
        frame = Frame(self)
        frame.pack(side = TOP, fill = BOTH, expand=True)
        frame1 = Frame(frame, bootstyle= INFO)
        frame1.place(x=10,y=0,width=1180,height=650)

        lblframe1 = Labelframe(frame1,text="Formulario",bootstyle= PRIMARY)
        lblframe1.pack(side=TOP, fill=BOTH, expand=True)

        # FORMULARIO
        # campos actuales
        self.e_usuario = Label(lblframe1, text="Usuario: ", bootstyle=PRIMARY)
        self.e_usuario.place(x=5, y=0)
        self.e_vusuario = Label(lblframe1, text=self.user.nombre, bootstyle=PRIMARY)
        self.e_vusuario.place(x=150, y=0)

        self.e_correoe = Label(lblframe1, text="Correo electrónico: ", bootstyle=PRIMARY)
        self.e_correoe.place(x=5, y=40)
        self.e_vcorreoe = Label(lblframe1, text=self.user.correo, bootstyle=PRIMARY)
        self.e_vcorreoe.place(x=150, y=40)

        self.e_localidad = Label(lblframe1, text="Localidad: ", bootstyle=PRIMARY)
        self.e_localidad.place(x=5, y=80)
        localidad = self.user.localidad if self.user.localidad is not None else "Ninguna"
        self.e_vlocalidad = Label(lblframe1, text=localidad, bootstyle=PRIMARY)
        self.e_vlocalidad.place(x=150, y=80)
        
        self.e_nacimiento = Label(lblframe1, text="Fecha nacimiento: ", bootstyle=PRIMARY)
        self.e_nacimiento.place(x=5, y=120)
        nacimiento = self.user.nacimiento if self.user.nacimiento is not None else "Ninguna"
        self.e_vnacimiento = Label(lblframe1, text=nacimiento, bootstyle=PRIMARY)
        self.e_vnacimiento.place(x=150, y=120)

        self.e_fotoperfil = Label(lblframe1, text="Foto de perfil: ", bootstyle=PRIMARY)
        self.e_fotoperfil.place(x=5, y=205)

        self.lblimageperfil = Frame(self.principal, bootstyle = INFO)
        self.lblimageperfil.place(x=150, y=205, width=70, height=70)

        self.labelPerfil = Label(self.lblimageperfil, image=self.perfil)
        self.labelPerfil.pack(side=tk.TOP, fill=BOTH, expand=True)
        
        self.btneditar = Button(lblframe1, text="Editar cuenta", command=self.editar, bootstyle=SUCCESS)
        self.btneditar.place(x=5, y=380, width=135)            

        # campos nuevos a modificar
        self.e_newusuario = self.entry_label(lblframe1, 700, 0, "Usuario: ")
        self.e_newpassw = self.entry_label(lblframe1, 700, 40, "Nueva contraseña: ")
        self.e_newpasswconf = self.entry_label(lblframe1, 700, 80, "Confirmar nueva contraseña: ")
        self.e_newcorreoe = self.entry_label(lblframe1, 700, 120, "Nuevo correo electrónico: ")
        self.e_newlocalidad = self.entry_label(lblframe1, 700, 160, "Localidad: ")
        self.e_newnacimiento = self.entry_label(lblframe1, 700, 200, "Fecha nacimiento: ")
        
        self.btnfotoperfil = Button(lblframe1, text="Elegir foto perfil", command=self.open_file_dialog)
        self.btnfotoperfil.configure(state="disabled")
        self.btnfotoperfil.place(x=700, y=270, width=135)
        
        self.lblimageperfil = Frame(self.principal, bootstyle = INFO)
        self.lblimageperfil.place(x=920, y=270, width=70, height=70)

        self.labelPerfil = Label(self.lblimageperfil, image=self.perfil)
        self.labelPerfil.pack(side=tk.TOP, fill=BOTH, expand=True)

        # botones de opciones
        self.btnguardar = Button(lblframe1, text="Guardar cambios", bootstyle = SUCCESS, command=self.guardar_cambios)
        self.btnguardar.configure(state="disabled")
        self.btnguardar.place(x=700, y=400, width=150)

        self.btndescartar = Button(lblframe1, text="Descartar cambios", bootstyle = DANGER, command=self.descartar)
        self.btndescartar.configure(state="disabled")
        self.btndescartar.place(x=875, y=400, width=150)

        self.btneliminar = Button(lblframe1,text="Eliminar cuenta", command=self.eliminar_cuenta, bootstyle=DANGER)
        self.btneliminar.place(x=5, y=590,width=135)

    # HASH
    def do_hash(self, texto: str):
        hasher = hashlib.sha3_512()
        hasher.update(texto.encode('utf-8'))
        return hasher.hexdigest() 
    
    def ask_for_passw(self, texto, tipo):
        self.popup = tk.Toplevel(self.principal)
        self.popup.geometry("400x200")
        self.popup.resizable(False, False)
        self.popup.lift()
        ttk.Label(self.popup, text=texto).place(x=30,y=20)
        self.passw_entry = ttk.Entry(self.popup, show="*", width=30)
        self.passw_entry.place(x=80,y=65)
        self.passw_entry.focus_set()
        ttk.Button(self.popup, text="Confirmar", bootstyle = SUCCESS, command=lambda: self.check_pass(tipo)).place(x=300,y=160)
        
    def check_pass(self, tipo):
        user = self.database_manager.selectUserById(self.user_id)
        if self.do_hash(self.passw_entry.get()) == user.password: # porque guardo la contraseña hasheada
            Messagebox.show_info(title="Éxito", message="Contraseña correcta.", parent=self.popup)
            self.popup.destroy()
            if tipo =="guardar":
                self.guardar() # guardo cambios
            if tipo == "eliminar":
                self.eliminar() # elimino la cuenta
        else: 
            Messagebox.show_error(title="Error", message="Contraseña incorrecta. Inténtalo de nuevo", alert=True, parent=self.popup)
            self.popup.destroy()