from ttkbootstrap import * 
from add_libros import AddLibro
from add_otros import AddOtro
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox
from persistence.model import *
from persistence.repository.database_manager import DatabaseManager
import re 
from datetime import datetime

class AddEstantes(Frame):
    def __init__(self, id, lista_estantes: list, master = None):
        super().__init__(master)
        self.database_manager = DatabaseManager()
        self.user_id = id
        self.doc_id_editar = ""
        self.estantes = lista_estantes
        self.principal = master
        self.widgets()
        self.mostrar_estantes()
        self.mostrar_libros()
    
    def entry_label(self,frame,x,y,texto):
        lbl = Label(frame, text=texto,bootstyle=PRIMARY)
        lbl.place(x=x,y=y)

        if texto == "ID":
            entry = Entry(frame, bootstyle=(PRIMARY))
            entry.place(x=x+100, y=y, width=30)
        else:
            entry = Entry(frame, bootstyle=(PRIMARY))
            entry.place(x=x+100, y=y)
        return entry

    def comboboxea(self, frame, x, y, texto, opciones):
        lbl = Label(frame, text=texto,bootstyle=PRIMARY)
        lbl.place(x=x,y=y)

        combo = Combobox(frame, values=opciones)
        if len(opciones) != 0:
            combo.current(0)
        combo.place(x=x+100,y=y)
        return combo

    def validar(self):
        if self.e_nombre.get() == "" or self.e_tipo.get() == "":
            Messagebox.show_error(title="Error", message="Faltan campos obligatorios", alert=True)
            return False
        elif len(self.e_nombre.get()) == 0:
            Messagebox.show_error(title="Error", message="El nombre es un campo obligatorio", alert=True)
            return False 
        return True

    def mostrar_estantes(self):
        dato_e = []
        datosEstantes = self.database_manager.selectAllEstantesByIdOwner(self.user_id) # obtengo los estantes pertenezcan al usuario
        if len(datosEstantes) != 0:
            for estante in datosEstantes:
                fila = [estante.id, estante.nombre, estante.tematica, estante.tipo, estante.tamano]
                dato_e.append(fila)
        self.tableviewEstantes.build_table_data(self.coldataEstantes, dato_e)

    def mostrar_libros(self):
        formato = ""
        dato_l = []
        datosDocumentos = self.database_manager.selectAllDocumentosLibros(self.user_id) # obtengo todos los documentos que sean libros y pertenezcan al usuario
        if len(datosDocumentos) != 0:
            for documento in datosDocumentos:
                datosLibro = self.database_manager.selectLibrosById(documento.id) # obtengo los datos del libro
                if documento.formato_id == 1000:
                    formato = "Físico"
                else:
                    formato = "PDF"
                fila = [documento.id, documento.titulo, formato, datosLibro[0].tematica]
                dato_l.append(fila)
        self.tableviewLibros.build_table_data(self.coldataLibros, dato_l)

    def guardar(self):
        if self.validar(): #validar datos de los campos antes de guardar
            estante = Estante()
            estante.nombre = self.e_nombre.get()
            estante.propietario_id = self.user_id
            estante.tematica = self.e_tematica.get()
            estante.tamano = 0 # a la hora de crear los estantes no tienen ningún tipo de libro
            estante.fecha_creacion = datetime.now().date()
            estante.fecha_modificacion = None
            estante.tipo = self.e_tipo.get()
            if self.is_new: # si no es una actualización
                #añadimos el estante
                self.database_manager.insertEstante(estante)
                Messagebox.show_info(title="Éxito", message="Datos guardados con éxito")
            else: # es una actualización
                valor = Messagebox.show_question(title="Alerta", message="¿Estás seguro de que deseas actualizar el estante?", alert=True)
                if valor == "Sí":
                    nueva_modificacion = datetime.now().date()
                    self.database_manager.updateEstante(self.doc_id_editar, self.e_nombre.get(), self.e_tematica.get(), self.e_tipo.get(), nueva_modificacion)
                    self.is_new = True
                    Messagebox.show_info(title="Éxito", message="Datos actualizados con éxito")
                self.btneditar.configure(state="disable")
                self.btneliminar.configure(state="disable")
            self.mostrar_estantes()
            self.limpiar_estantes()

    def add_libro_estante(self):
        pass

    def delete_libro_estante(self):
        #nombre_estante = self.combo_estantes_delete.get() # obtengo el nombre del estante del que voy a eliminar el libro
        estante = self.database_manager.selectEstanteByName(self.combo_estantes_delete.get())
        self.database_manager.deleteDocumentoEstante(self.doc_id_editar, estante.id)
        self.database_manager.updateEstanteSize(estante.tamano-1)

    def fill_estantes_add(self):
        nombres_estantes = []
        estantes = self.database_manager.selectAllEstantesByIdOwner(self.user_id) # obtengo todos los estantes creados para el usuario
        for estante in estantes:
            nombres_estantes.append(estante.nombre)
        self.combo_estantes_add['values'] = nombres_estantes

    def fill_estantes_delete(self):
        nombres_estantes = []
        estantes = self.database_manager.selectEstantesLibro(self.doc_id_editar) # obtengo los estantes en los que está el libro
        for estante in estantes:
            nombres_estantes.append(estante.nombre)
        self.combo_estantes_delete['values'] = nombres_estantes

    def seleccionar(self):
        self.limpiar_libros()
        dato = self.tableviewLibros.view.item(self.tableviewLibros.view.selection())["values"]
        self.doc_id_editar = int(dato[0]) # id del libro 
        documento = self.database_manager.selectDocumentById(self.doc_id_editar) # obtengo el documento con ese id
        self.e_id.insert(0, self.doc_id_editar)
        self.e_titulo.insert(0, documento.titulo)
        if documento.formato_id == 1000:
            self.e_formato.insert(0, "Físico")
        else:
            self.e_formato.insert(0, "PDF")
        # relleno los combobox con los respectivos estantes
        self.fill_estantes_add()
        self.fill_estantes_delete()
        self.btnadd_libro.configure(state="normal")
        self.btneliminar_libro.configure(state="normal")

    def limpiar_estantes(self):
        self.e_nombre.delete(0, END)
        self.e_tematica.delete(0, END)
        self.e_tipo.delete(0, END)
    
    def limpiar_libros(self):
        self.e_id.delete(0, END)
        self.e_titulo.delete(0, END)
        self.e_formato.delete(0, END)

    def editar(self):
        self.is_new = False
        self.limpiar_estantes()
        dato = self.tableviewEstantes.view.item(self.tableviewEstantes.view.selection())["values"]
        self.doc_id_editar = int(dato[0]) # id del estante a editar
        estante = self.database_manager.selectEstanteById(self.doc_id_editar)
        self.e_nombre.insert(0, estante.nombre)
        self.e_tematica.insert(0, estante.tematica)
        self.e_tipo.current(0)

    def eliminar(self):
        dato = self.tableviewEstantes.view.item(self.tableviewEstantes.view.selection())["values"]
        valor = Messagebox.show_question(title="Alertar", message="¿Estás seguro de que deseas eliminar este estante?", alert=True)
        if valor == "Sí": #se elimina
            self.database_manager.deleteEstanteById(int(dato[0]))
        Messagebox.show_info(title="Éxito", message="Estante eliminado con éxito")
        
        self.mostrar_estantes()
        self.btneditar.configure(state="disable")
        self.btneliminar.configure(state="disable")

    def eventos_estantes(self, event):
        print(self.tableviewEstantes.view.item(self.tableviewEstantes.view.selection())["values"])
        self.btneditar.configure(state="normal")
        self.btneliminar.configure(state="normal")

    def eventos_libros(self, event):
        print(self.tableviewEstantes.view.item(self.tableviewLibros.view.selection())["values"])
        self.btnseleccionar_libro.configure(state="normal")

    def widgets(self):
        # FRAMES
        frame = Frame(self)
        frame.pack(side = TOP, fill = BOTH, expand=True)

        frame1 = Frame(frame, bootstyle= INFO)
        frame1.place(x=10, y=0, width=350, height=300)

        lblframe1 = Labelframe(frame1, text="Formulario estante", bootstyle= PRIMARY)
        lblframe1.pack(side=TOP, fill=BOTH, expand=True)

        frame2 = Frame(frame, bootstyle=DANGER)
        frame2.place(x=370, y=0, width=880, height=300)

        lblframe2 = LabelFrame(frame2, text="Datos estantes", bootstyle=SUCCESS)
        lblframe2.pack(side=TOP, fill=BOTH, expand=True)

        frame3 = Frame(frame, bootstyle= INFO)
        frame3.place(x=10, y=310, width=350, height=340)

        lblframe3 = LabelFrame(frame3, text="Añadir/Eliminar libro", bootstyle=PRIMARY)
        lblframe3.pack(side=TOP, fill=BOTH, expand=True)

        frame4 = Frame(frame, bootstyle= INFO)
        frame4.place(x=370, y=310, width=880, height=340)

        lblframe4 = LabelFrame(frame4, text="Datos libros", bootstyle=SUCCESS)
        lblframe4.pack(side=TOP, fill=BOTH, expand=True)

        # FORMULARIO CREAR ESTANTE
        #campos de estante
        self.e_nombre = self.entry_label(lblframe1, 5, 0, "Nombre")
        self.e_tematica = self.entry_label(lblframe1, 5, 40, "Temática")
        opciones_tipo = ["Libros", "Otros", "Libros/Otros"] 
        self.e_tipo = self.comboboxea(lblframe1, 5, 80, "Tipo", opciones_tipo)

        self.btnguardar = Button(lblframe1, text="Guardar", command=self.guardar)
        self.btnguardar.place(x=10, y=150, width=135)

        self.btneditar = Button(lblframe1, text="Editar", command=self.editar, bootstyle=SUCCESS)
        self.btneditar.configure(state= "disable")
        self.btneditar.place(x=10, y=190, width=135)

        self.btneliminar = Button(lblframe1, text="Eliminar", command=self.eliminar, bootstyle=DANGER)
        self.btneliminar.configure(state= "disable")
        self.btneliminar.place(x=10, y=230, width=135)

        # FORMULARIO AÑADIR/ELIMINAR LIBRO
        self.e_id = self.entry_label(lblframe3, 5, 0, "ID")
        self.e_titulo = self.entry_label(lblframe3, 5, 40, "Título")
        self.e_formato = self.entry_label(lblframe3, 5, 80, "Formato")
        
        self.btnseleccionar_libro = Button(lblframe3, text="Seleccionar", command=self.seleccionar, bootstyle=SUCCESS)
        self.btnseleccionar_libro.configure(state= "disable")
        self.btnseleccionar_libro.place(x=5, y=160, width=100)

        self.btnadd_libro = Button(lblframe3, text="Añadir", command=self.add_libro_estante, bootstyle=SUCCESS)
        self.btnadd_libro.configure(state= "disable")
        self.btnadd_libro.place(x=5, y=220, width=100)
        self.combo_estantes_add = Combobox(lblframe3, values=self.estantes)
        if len(self.estantes) != 0:
            self.combo_estantes_add.current(0)
        self.combo_estantes_add.place(x=125, y=220)
        #self.e_estantes_add = self.comboboxea(lblframe3, 5, 160, "Estantes", opciones_tipo)

        self.btneliminar_libro = Button(lblframe3, text="Eliminar", command=self.delete_libro_estante, bootstyle=DANGER)
        self.btneliminar_libro.configure(state= "disable")
        self.btneliminar_libro.place(x=5, y=280, width=100)
        self.combo_estantes_delete = Combobox(lblframe3, values=self.estantes)
        if len(self.estantes) != 0:
            self.combo_estantes_delete.current(0)
        self.combo_estantes_delete.place(x=125, y=280)

        # TABLA LBLFRAME2
        self.coldataEstantes = [
            {"text":"ID", "width":200},
            {"text":"Nombre", "width":300},
            {"text":"Temática", "stretch":True},
            {"text":"Tipo", "width":50},
            {"text":"Tamaño", "width":30},
        ]
        self.tableviewEstantes = Tableview(lblframe2, 
                              paginated=True,
                              searchable=True,
                              bootstyle=(SUCCESS),
                              stripecolor=("snow", "black"), #"cyan", None
                              autoalign=True,
                              autofit=True,
                              height=15,
                              delimiter=";")
        self.tableviewEstantes.pack(fill=BOTH, expand=True,padx=5,pady=5)
        self.tableviewEstantes.view.bind("<Double-1>", self.eventos_estantes)
        self.tableviewEstantes.align_column_center()

        # TABLA LBLFRAME4
        self.coldataLibros = [
            {"text":"ID", "width":200},
            {"text":"Título", "stretch":True},
            {"text":"Formato", "width":200},
            {"text":"Temática", "width":50},
        ]
        self.tableviewLibros = Tableview(lblframe4, 
                              paginated=True,
                              searchable=True,
                              bootstyle=(SUCCESS),
                              stripecolor=("snow", "black"), #"cyan", None
                              autoalign=True,
                              autofit=True,
                              height=15,
                              delimiter=";")
        self.tableviewLibros.pack(fill=BOTH, expand=True,padx=5,pady=5)
        self.tableviewLibros.view.bind("<Double-1>", self.eventos_libros)
        self.tableviewLibros.align_column_center()

    