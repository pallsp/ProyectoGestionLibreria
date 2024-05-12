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

from ttkbootstrap import * 
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox

from ttkbootstrap import * 
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox

class Ajustes(Frame):
    def __init__(self, id, master = None):
        super().__init__(master)
        self.database_manager = DatabaseManager() # establecer el gestor de la base de datos
        self.user_id = id
        self.user: Usuario = self.database_manager.selectUserById(self.user_id)
        #super().__init__(themename="superhero", size=(1260, 700), title="Interfaz moderna") #proporcion 1.8
        self.principal = master
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
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            print("Archivo seleccionado: ", self.image_path)
            self.set_image_perfil(self.image_path)
            self.set_image_frame()

    # GUARDAR CAMBIOS
    def guardar_cambios(self):
        if self.validar(): # validar los campos
            self.popup = tk.Toplevel(self.principal)
            self.popup.geometry("400x200")
            self.popup.resizable(False, False)
            ttk.Label(self.popup, text="Introduce la contraseña para confirmar los cambios: ").place(x=30,y=20)
            self.passw_entry = ttk.Entry(self.popup, show="*", width=30)
            self.passw_entry.place(x=80,y=65)
            self.passw_entry.focus_set()
            ttk.Button(self.popup, text="Confirmar", bootstyle = SUCCESS, command=self.check_pass).place(x=300,y=160)

    def validar(self):
        if self.e_newusuario == "" and self.e_newpassw == "" and self.e_newpasswconf == "" and self.e_newcorreoe == "":
            Messagebox.show_error(title="Error",message="Están todos los campos vacíos", alert=True)
            return False
        elif self.e_newpassw != self.e_newpasswconf:
            Messagebox.show_error(title="Error",message="Las contraseñas no coinciden", alert=True)
            return False
        return True

    def check_pass(self):
        user = self.database_manager.selectUserById(self.user_id)
        if self.do_hash(self.passw_entry.get()) == user.password: # porque guardo la contraseña hasheada
            Messagebox.show_info(title="Éxito",message="Contraseña correcta. Cambios confirmados")
            self.limpiar()
            self.popup.destroy()
            self.guardar() # guardo cambios
        else: 
            Messagebox.show_error(title="Error",message="Contraseña incorrecta. Inténtalo de nuevo", alert=True)
            self.popup.destroy()
            # no guardo cambios

    def guardar(self):
        self.database_manager.updateUsuario(self.user_id, self.e_newusuario, self.e_newpassw, self.e_newcorreoe, self.image_path)
        self.limpiar()
        Messagebox.show_info(title="Éxito",message="Cambios guardados con éxito")
    
    # DESCARTAR CAMBIOS
    def descartar(self):
        self.limpiar()

    # EDITAR (NECESARIO PULSAR PARA PODER GUARDAR O DESCARTAR)
    def editar(self):
        self.btnguardar.configure(state="active")
        self.btndescartar.configure(state="active")
        #dato = self.tableview.view.item(self.tableview.view.selection())["values"]
        #self.idlibro = int(dato[0])
        #self.e_titulo.insert(0,dato[1])
        #self.e_autor.insert(0,dato[2])
        #self.e_idioma.insert(0,dato[3])
        #self.e_editorial.insert(0,dato[4])

    def eliminar(self):
        dato = self.tableview.view.item(self.tableview.view.selection())["values"][0]
        valor = Messagebox.show_question(title="Alertar",message="¿Estás seguro de que deseas eliminar el libro?",alert=True)
        if valor == "Sí":
            pass
            #Datos.guardar("DELETE FROM libros WHERE id = ?",(dato,))
        self.mostrar()
        self.btneditar.configure(state="disable")
        self.btneliminar.configure(state="disable")

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

    def limpiar(self):
        self.e_newusuario.delete(0, END)
        self.e_newpassw.delete(0, END)
        self.e_newpasswconf.delete(0, END)
        self.e_newcorreoe.delete(0, END)

    def widgets(self):
        frame = Frame(self)
        frame.pack(side = TOP, fill = BOTH, expand=True)
        frame1 = Frame(frame, bootstyle= INFO)
        frame1.place(x=10,y=0,width=1180,height=650)

        lblframe1 = Labelframe(frame1,text="Formulario",bootstyle= PRIMARY)
        lblframe1.pack(side=TOP, fill=BOTH, expand=True)

        # FORMULARIO
        # campos actuales
        self.e_usuario = Label(lblframe1, text="Usuario", bootstyle=PRIMARY)
        self.e_usuario.place(x=5,y=0)
        self.e_vusuario = Label(lblframe1, text=self.user.nombre, bootstyle=PRIMARY)
        self.e_vusuario.place(x=150,y=0)

        self.e_correoe = Label(lblframe1, text="Correo electrónico", bootstyle=PRIMARY)
        self.e_correoe.place(x=5,y=40)
        self.e_vcorreoe = Label(lblframe1, text=self.user.correo, bootstyle=PRIMARY)
        self.e_vcorreoe.place(x=150,y=40)

        self.e_fotoperfil = Label(lblframe1, text="Foto de perfil", bootstyle=PRIMARY)
        self.e_fotoperfil.place(x=5,y=125)

        self.lblimageperfil = Frame(self.principal, bootstyle = INFO)
        self.lblimageperfil.place(x=150, y=125, width=70, height=70)

        self.labelPerfil = Label(self.lblimageperfil, image=self.perfil)
        self.labelPerfil.pack(side=tk.TOP, fill=BOTH, expand=True)
        
        self.btneditar = Button(lblframe1,text="Editar", command=self.editar, bootstyle=SUCCESS)
        #self.btneditar.configure(state= "disable")
        self.btneditar.place(x=5, y=380, width=135)

        # campos nuevos a modificar
        self.e_newusuario = self.entry_label(lblframe1,700,0,"Usuario")
        self.e_newpassw = self.entry_label(lblframe1,700,40,"Nueva contraseña")
        self.e_newpasswconf = self.entry_label(lblframe1,700,80,"Confirmar nueva contraseña")
        self.e_newcorreoe = self.entry_label(lblframe1,700,120,"Nuevo correo electrónico")

        self.btnfotoperfil = Button(lblframe1, text="Elegir foto perfil", command=self.open_file_dialog)
        self.btnfotoperfil.place(x=700, y=190, width=135)
        
        self.lblimageperfil = Frame(self.principal, bootstyle = INFO)
        self.lblimageperfil.place(x=920, y=190, width=70, height=70)

        self.labelPerfil = Label(self.lblimageperfil, image=self.perfil)
        self.labelPerfil.pack(side=tk.TOP, fill=BOTH, expand=True)

        # botones de opciones
        self.btnguardar = Button(lblframe1, text="Guardar cambios", bootstyle = SUCCESS, command=self.guardar_cambios)
        self.btnguardar.configure(state="disable")
        self.btnguardar.place(x=700,y=380,width=150)

        self.btndescartar = Button(lblframe1, text="Descartar cambios", bootstyle = DANGER, command=self.descartar)
        self.btndescartar.configure(state="disable")
        self.btndescartar.place(x=875, y=380, width=150)

        self.btneliminar = Button(lblframe1,text="Eliminar",command=self.eliminar,bootstyle=DANGER)
        self.btneliminar.configure(state= "disable")
        self.btneliminar.place(x=10,y=590,width=135)

    # HASH
    def do_hash(self, texto: str):
        hasher = hashlib.sha3_512()
        hasher.update(texto.encode('utf-8'))
        return hasher.hexdigest() 