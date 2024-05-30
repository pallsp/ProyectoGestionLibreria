import tkinter as tk
from tkinter import *
from ttkbootstrap import * 
from ttkbootstrap.dialogs import Messagebox
from data import Datos
from crear_documentos import AddDocumentos
from ajustes import Ajustes
import util.generic as utl_img
from persistence.repository.database_manager import DatabaseManager
from persistence.model import *
from tkinter import font 
from ttkbootstrap import font
from crear_estantes import AddEstantes
import sys
import hashlib
from ver_biblioteca import VerBiblioteca
from visor import VisorPDF

class App(Window):
    def __init__(self, themename = "superhero"):
        super().__init__(size=(1520, 810), title="Menú principal", resizable=(False, False)) 
        if len(sys.argv) > 1:
            self.user_id = int(sys.argv[1])
        else:
            self.user_id = 1
        self.database_manager = DatabaseManager()
        self.estilo = Style(theme=themename)
        self.tema_actual = themename
        #self.user_id = 1
        self.user: Usuario = self.database_manager.selectUserById(self.user_id) # obtengo el usuario a partir del user_id
        self.perfil = ""
        self.bannerinicio = ""
        self.logotop = ""
        self.estantes = self.database_manager.selectAllEstantesByIdOwner(self.user_id) # lista con los estantes
        #self.banner = utl_img.leer_imagen("/home/pablo/PROYECTO/App/imagenes/banner_recortado.png", (276,70)) # fuente Ruda color #2e4b4b
        #self.set_image_perfil("/home/pablo/Escritorio/ProyectoFinalDAM/LibreriaGestion/login/sidebar_menu/imagenes/libreriologo.png") # foto predeterminada SE PUEDE CAMBIAR
        self.set_images(self.user.foto)
        self.widgets()
        self.open_inicio()
        self.idlibro = -1
        self.set_icon()
        
    def set_icon(self):
        self.iconphoto(False, tk.PhotoImage(file="/home/pablo/PROYECTO/imagenes/libreriologo.png")) 

    def set_images(self, path):
        self.perfil = utl_img.leer_imagen(path, (70, 70))
        self.bannerinicio = utl_img.leer_imagen("/home/pablo/PROYECTO/imagenes/otrolibrerio.png", (600, 300))
        self.logotop = utl_img.leer_imagen("/home/pablo/PROYECTO/imagenes/partelogo.png", (65,65))
        
    def entry_label(self,frame,x,y,texto):
        lbl = Label(frame, text=texto,bootstyle=PRIMARY)
        lbl.place(x=x,y=y)

        entry = Entry(frame, bootstyle=(PRIMARY))
        entry.place(x=x+100,y=y)
        return entry
    
    def comboboxea(self, frame, x, y, texto, opciones):
        lbl = Label(frame, text=texto,bootstyle=PRIMARY)
        lbl.place(x=x,y=y)

        combo = Combobox(frame, values=opciones)
        combo.current(0)
        combo.place(x=x+100,y=y)
        return combo

    def validar(self, titulo, autor, idioma, editorial):
        if len(titulo) == 0:
            return Messagebox.show_error(title="Error", message="El título es un campo obligatorio", alert=True)

    def mostrar(self):
        sql = "SELECT * FROM libros"
        dato = Datos.recuperar(sql,parametros=())
        self.tableview.build_table_data(self.coldata,dato)

    def guardar(self):
        titulo = self.e_titulo.get()
        autor = self.e_autor.get()
        idioma = self.e_idioma.get()
        editorial = self.e_editorial.get()
        if titulo.isdigit():
            self.titulo.delete(0, END)
            return Messagebox.show_error(title="Error",message="Ingresar un nombre válido para el producto", alert=True)
        if len(titulo) == 0:
            return Messagebox.show_error(title="Error", message="El título es un campo obligatorio", alert=True)
        if self.idlibro == -1:
            sql = "INSERT INTO libros (id,titulo,autor,idioma,editorial) VALUES (NULL,?,?,?,?)"
            parametros = (titulo,autor,idioma,editorial)
            try:
                Datos.guardar(sql,parametros)
            except Exception as e:
                print(f"Error: {e}")
                Messagebox.show_error(tittle="Error",message="El libro ya esta registrado",alert=True)
        else:
            valor = Messagebox.show_question(title="Alerta",message="¿Estás seguro de que deseas actualizar el libro?",alert=True)
            if valor == "Sí":
                sql = "UPDATE libros SET titulo = ?, autor = ?, idioma = ?, editorial = ? WHERE id = ?"
                parametros = (titulo,autor,idioma,editorial,self.idlibro)
                Datos.guardar(sql,parametros)
                self.idlibro = -1
        self.mostrar()
        self.limpiar()
        self.btneditar.configure(state="disable")
        self.btneliminar.configure(state="disable")

    def limpiar(self):
        self.e_titulo.delete(0, END)
        self.e_autor.delete(0, END)
        self.e_idioma.delete(0, END)
        self.e_editorial.delete(0, END)

    def editar(self):
        self.limpiar()
        dato = self.tableview.view.item(self.tableview.view.selection())["values"]
        self.idlibro = int(dato[0])
        self.e_titulo.insert(0,dato[1])
        self.e_autor.insert(0,dato[2])
        self.e_idioma.insert(0,dato[3])
        self.e_editorial.insert(0,dato[4])

    def eliminar(self):
        dato = self.tableview.view.item(self.tableview.view.selection())["values"][0]
        valor = Messagebox.show_question(title="Alertar",message="¿Estás seguro de que deseas eliminar el libro?",alert=True)
        if valor == "Sí":
            Datos.guardar("DELETE FROM libros WHERE id = ?",(dato,))
        self.mostrar()
        self.btneditar.configure(state="disable")
        self.btneliminar.configure(state="disable")

    def eventos(self,event):
        #if len(self.tableview.view.item(self.tableview.view.selection())["values"])!=0:
        self.btneditar.configure(state="normal")
        self.btneliminar.configure(state="normal")
            #print(self.tableview.view.item(self.tableview.view.selection())["values"])
    
    # Cambiar visibilidad del menú lateral
    def toggle_menu_lateral(self):
        if self.frameLateral.winfo_ismapped():   
            self.frameLateral.place_forget()
            self.lblFrameLateral.pack_forget()
            self.framePrincipal.place(x=0,y=100,width=1520,height=710)
        else:
            self.frameLateral.place(x=0,y=100,width=250,height=710)
            self.lblFrameLateral.pack(side=TOP, fill=BOTH, expand=True)
            self.framePrincipal.place(x=260,y=100,width=1260,height=710)

    def cambiar_tema(self): # #222222
        # Cambiar el tema entre 'superhero' y 'darkly'
        self.tema_actual = 'darkly' if self.tema_actual == 'superhero' else 'superhero'
        self.estilo.theme_use(self.tema_actual)
        if self.tema_actual == 'superhero':
            self.logotop = utl_img.leer_imagen("/home/pablo/PROYECTO/imagenes/partelogo.png", (65,65))
            self.label_logotop = Label(self.frameimagetop, image=self.logotop)
            self.label_logotop.place(x=0, y=0)
        else:
            self.logotop = utl_img.leer_imagen("/home/pablo/PROYECTO/imagenes/partelogo_darkly.png", (65,65))
            self.label_logotop = Label(self.frameimagetop, image=self.logotop)
            self.label_logotop.place(x=0, y=0)

    def widgets(self):
        # FRAMES
        self.frame = Frame(self)
        self.frame.pack(side = TOP, fill = BOTH, expand=True)

        self.frameTop = Frame(self.frame, bootstyle= INFO)
        self.frameTop.place(x=0, y=0, width=1520, height=100)

        self.frameLateral = Frame(self.frame, bootstyle= INFO)
        self.frameLateral.place(x=0, y=100, width=250, height=710)

        self.framePrincipal = Frame(self.frame, bootstyle= INFO)
        self.framePrincipal.place(x=260, y=100, width=1260, height=710)

        self.lblFrameTop = Labelframe(self.frameTop, text="Menú Top", bootstyle= PRIMARY)
        self.lblFrameTop.pack(side=TOP, fill=BOTH, expand=True)

        self.lblFrameLateral = Labelframe(self.frameLateral, text="Menú lateral", bootstyle= PRIMARY)
        self.lblFrameLateral.pack(side=TOP, fill=BOTH, expand=True)

        self.lblFramePrincipal = Labelframe(self.framePrincipal, text="Pantalla principal", bootstyle= PRIMARY)
        self.lblFramePrincipal.pack(side=TOP, fill=BOTH, expand=True)

        # ELEMENTOS FRAME TOP 
        
        # Crear un widget con el icono personalizado 
        font_awesome = font.Font(family='FontAwesome', size=12)
        self.btnocultar = tk.Button(self.lblFrameTop, text="\uf0c9", font=font_awesome, command=self.toggle_menu_lateral, bd=0, bg="#df5553", fg="white")
        self.btnocultar.place(x=210, y=40)

        self.lblimageperfil = Frame(self.lblFrameTop, bootstyle = INFO)
        self.lblimageperfil.place(x=10, y=0, width=70, height=70)

        self.labelPerfil = Label(self.lblimageperfil, image=self.perfil)
        self.labelPerfil.pack(side=tk.TOP, fill=BOTH, expand=True)
        
        self.btninfo = tk.Button(self.lblFrameTop, text="\u24D8", font=font_awesome, command=self.open_info, bd=0, bg="#df5553", fg="white")
        self.btninfo.place(x=1420, y=5, width=30, height=30) 

        self.btnlicense = tk.Button(self.lblFrameTop, text=u"\U0001F12F", font=font_awesome, command=self.open_license, bd=0, bg="#df5553", fg="white")
        self.btnlicense.place(x=1460, y=5, width=30, height=30) 

        label_titulo = ttk.Label(text="LIBRERIO BIBLIOTECA", font=("Ruda", 30), foreground="#dc3545")
        label_titulo.place(x=560, y=30, width=420, height=60)
        label_contacto = Label(text="libreriocontacto@gmail.com", bootstyle = LIGHT)
        label_contacto.place(x=1320, y=70)
        
        self.frameimagetop = Frame(self.lblFrameTop, bootstyle = INFO)
        self.frameimagetop.place(x=1010, y=5, width=65, height=65)

        self.label_logotop = Label(self.frameimagetop, image=self.logotop)
        self.label_logotop.place(x=0, y=0)
        #self.label_logotop.pack(side=tk.TOP, fill=BOTH, expand=True)

        # BOTONES MENU LATERAL
        btndocumentos = Button(self.lblFrameLateral, text="Gestionar documentos", bootstyle = WARNING, command=self.ver_documentos)
        btndocumentos.place(x=30, y=10, width=200)

        self.btnestante = Button(self.lblFrameLateral, text="Gestionar estantes", bootstyle = WARNING, command=lambda: self.show_confirm_passw("crear estantes"))
        self.btnestante.place(x=30, y=70, width=200)

        self.btnbiblioteca = Button(self.lblFrameLateral, text="Ver biblioteca", bootstyle = WARNING, command=lambda: self.show_confirm_passw("biblioteca"))
        self.btnbiblioteca.place(x=30, y=130, width=200)

        self.btnvisor = Button(self.lblFrameLateral, text="Visor PDF", bootstyle = WARNING, command=lambda: self.show_confirm_passw("visor"))
        self.btnvisor.place(x=30, y=190, width=200)

        self.boton_cambiar_tema = ttk.Checkbutton(self.frameLateral, text="Modo oscuro", command=self.cambiar_tema, bootstyle="info-round-toggle")
        self.boton_cambiar_tema.place(x=30, y=280)

        self.btninicio = tk.Button(self.lblFrameLateral, text="\uf015", font=font_awesome, command=self.open_inicio, bd=0, bg="#df5553", fg="white")
        self.btninicio.place(x=115, y=400)
        
        self.btnmanual = Button(self.lblFrameLateral, text="Manual usuario", bootstyle = WARNING, command=self.open_manual)
        self.btnmanual.place(x=30, y=450, width=200)

        self.btnajustes = Button(self.lblFrameLateral,text="Ajustes", bootstyle = WARNING, command=lambda: self.show_confirm_passw("ajustes")) #command=self.open_ajustes
        self.btnajustes.place(x=30, y=650, width=200)

        self.lblimageperfil_lat = Frame(self.lblFrameLateral, bootstyle = INFO)
        self.lblimageperfil_lat.place(x=30, y=560, width=70, height=70)

        self.labelPerfil_lat = Label(self.lblimageperfil_lat, image=self.perfil)
        self.labelPerfil_lat.pack(side=tk.TOP, fill=BOTH, expand=True)

        lbl_nombre = Label(self.lblFrameLateral, text=self.user.nombre, bootstyle=PRIMARY)
        lbl_nombre.place(x=120,y=580)

    def open_info(self):
        self.popup = tk.Toplevel(self.lblFramePrincipal)
        self.popup.geometry("300x100")
        self.popup.resizable(False, False)
        ttk.Label(self.popup, text="Autor: Pablo Pallàs").place(x=30, y=20)
        ttk.Label(self.popup, text="Versión: 1.0").place(x=30, y=60)

    def open_license(self):
        self.popup = tk.Toplevel(self.lblFramePrincipal)
        self.popup.geometry("600x800")
        self.popup.resizable(False, False)
        self.popup.title("Licencia GNU GPLv3")

        scrollbar = ttk.Scrollbar(self.popup)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_area = tk.Text(self.popup, wrap="word", yscrollcommand=scrollbar.set)
        text_area.pack(fill=tk.BOTH, expand=True)

        # leemos el .txt con la licencia
        with open("/home/pablo/PROYECTO/App/license/license.txt", "r") as file:
            text = file.read()
        # insertamos el texto en el widget text
        text_area.insert(tk.END, text)
        # configuramos la barra de desplazamiento para que se mueva junto con el texto 
        scrollbar.config(command=text_area.yview)
    
    def open_visor(self):
        if len(self.database_manager.selectDocumentsByIdOwner(self.user_id)) == 0:
            Messagebox.show_info(title="Error", message="No hay documentos añadidos. Necesitas añadir documentos.", alert=True)
        else:
            self.limpiar_pantalla(self.lblFramePrincipal)
            pantalla_visor = VisorPDF(self.user_id, self.lblFramePrincipal)
            pantalla_visor.place(x=0, y=0, width=1260, height=710)
    
    def open_manual(self):
        pass

    def limpiar_pantalla(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()

    # CAMBIAR PANTALLAS
    def open_inicio(self):
        self.limpiar_pantalla(self.lblFramePrincipal)
        
        self.iniciobanner = Frame(self.lblFramePrincipal, bootstyle = INFO)
        self.iniciobanner.place(x=300, y=50, width=600, height=300)

        self.inicio_image = Label(self.iniciobanner, image=self.bannerinicio)
        self.inicio_image.pack(side=tk.TOP, fill=BOTH, expand=True)
        
        text_area_license = tk.Text(self.lblFramePrincipal, wrap="word")
        text_area_license.place(x=300, y=370, width=600, height=200)
        
        # leemos el .txt con la info a mostrar
        with open("/home/pablo/PROYECTO/App/license/mostrar.txt", "r") as file:
            text = file.read()
        text_area_license.insert(tk.END, text)
        
    def open_ajustes(self):
        self.limpiar_pantalla(self.lblFramePrincipal)
        pantalla_ajustes = Ajustes(self.user_id, self, self.lblFramePrincipal)
        pantalla_ajustes.place(x=0, y=0, width=1260, height=710)

    def ver_documentos(self):
        self.limpiar_pantalla(self.lblFramePrincipal)
        pantalla_documentos = AddDocumentos(self.user_id, self.lblFramePrincipal)
        pantalla_documentos.place(x=0, y=0, width=1260, height=710) # 260 100

    def nuevo_estante(self):
        self.limpiar_pantalla(self.lblFramePrincipal)
        pantalla_estantes = AddEstantes(self.user_id, self.lblFramePrincipal)
        pantalla_estantes.place(x=0, y=0, width=1260, height=710)

    def ver_biblioteca(self):
        if len(self.database_manager.selectAllEstantesByIdOwner(self.user_id)) == 0:
            Messagebox.show_info(title="Error", message="No hay estantes creados. Necesitas crear estantes.", alert=True, parent=self)
        else:
            self.limpiar_pantalla(self.lblFramePrincipal)
            pantalla_biblioteca = VerBiblioteca(self.user_id, self.lblFramePrincipal)
            pantalla_biblioteca.place(x=0, y=0, width=1260, height=710)
    
    # PARA SOLICITAR CONTRASEÑA
    def check_pass(self, tipo):
        estado = False
        #user = self.database_manager.selectUserById(self.user_id)
        if self.do_hash(self.passw_entry.get()) == self.user.password: # porque guardo la contraseña hasheada
            Messagebox.show_info(title="Éxito", message=f"Contraseña correcta. Puedes entrar a {tipo}.", parent=self.popup)
            estado = True
        else: 
            Messagebox.show_error(title="Error", message="Contraseña incorrecta. Inténtalo de nuevo", alert=True, parent=self.popup)
        self.popup.destroy()
        if estado and tipo == "crear estantes":
            self.nuevo_estante()
        elif estado and tipo == "ajustes":
            self.open_ajustes()
        elif estado and tipo == "biblioteca":
            self.ver_biblioteca()
        elif estado and tipo =="visor":
            self.open_visor()

    def show_confirm_passw(self, tipo):
        self.popup = tk.Toplevel(self.lblFramePrincipal)
        self.popup.geometry("400x200")
        self.popup.resizable(False, False)
        ttk.Label(self.popup, text=f"Introduce la contraseña para poder ir a {tipo}: ").place(x=30,y=20)
        self.passw_entry = ttk.Entry(self.popup, show="*", width=30)
        self.passw_entry.place(x=80,y=65)
        self.passw_entry.focus_set()
        ttk.Button(self.popup, text="Confirmar", bootstyle = SUCCESS, command=lambda: self.check_pass(tipo)).place(x=300,y=160)

    # HASH
    def do_hash(self, texto: str):
        hasher = hashlib.sha3_512()
        hasher.update(texto.encode('utf-8'))
        return hasher.hexdigest()

if __name__ == "__main__":
    app = App()
    app.mainloop()

#app = App()
#app.mainloop()