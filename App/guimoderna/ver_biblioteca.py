from ttkbootstrap import * 
from add_libros import AddLibro
from add_otros import AddOtro
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox
from persistence.model import *
from persistence.repository.database_manager import DatabaseManager
import re 
from datetime import datetime

class VerBiblioteca(Frame):
    def __init__(self, id, master = None):
        super().__init__(master)
        self.database_manager = DatabaseManager()
        self.user_id = id
        self.estantes = self.database_manager.selectAllEstantesByIdOwner(self.user_id)
        self.principal = master
        self.widgets()
    
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

    def mostrar_documentos(self):
        formato = ""
        dato_l = []
        datosDocumentos = self.database_manager.selectAllDocumentosLibros(self.user_id) # obtengo todos los documentos que sean libros y pertenezcan al usuario
        if len(datosDocumentos) != 0:
            for documento in datosDocumentos:
                #datosLibro = self.database_manager.selectLibroById(documento.id) # obtengo los datos del libro
                if documento.formato_id == 1000:
                    formato = "Físico"
                else:
                    formato = "PDF"
                fila = [documento.id, documento.titulo, formato, documento.tipo]
                dato_l.append(fila)
        self.tableviewDocs.build_table_data(self.coldataDocs, dato_l)

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
                Messagebox.show_info(title="Éxito", message="Estante guardado con éxito")
            else: # es una actualización
                valor = Messagebox.show_question(title="Alerta", message="¿Estás seguro de que deseas actualizar el estante?", alert=True)
                if valor == "Sí":
                    nueva_modificacion = datetime.now().date()
                    self.database_manager.updateEstante(self.doc_id_editar, self.e_nombre.get(), self.e_tematica.get(), self.e_tipo.get(), nueva_modificacion)
                    self.is_new = True
                    Messagebox.show_info(title="Éxito", message="Estante actualizado con éxito")
                self.btneditar.configure(state="disable")
                self.btneliminar.configure(state="disable")
            self.mostrar_estantes()
            self.limpiar_estantes()

    def add_doc_estante(self):
        estante = self.database_manager.selectEstanteByName(self.combo_estantes_add.get())
        if estante.tipo == "LIBROS/OTROS" or estante.tipo == self.e_tipo_doc.get().upper(): # si el estante es del mismo tipo que el documento o es LIBROS/OTROS
            if self.database_manager.selectEstanteLibro(self.doc_id_editar, estante.id) == None: # si no está ese documento en el estante lo puedo añadir
                self.database_manager.insertDocumentoEstante(self.doc_id_editar, estante.id)
                self.database_manager.updateEstanteSize(estante.id, estante.tamano+1)
                Messagebox.show_info(title="Éxito", message="Documento agregado con éxito del estante")
            else: # si está ya no dejo que se pueda añadir de nuevo 
                Messagebox.show_error(title="Error", message="El documento ya pertenece al estante", alert=True)
        else:
            Messagebox.show_error(title="Error", message="El estante no admite este tipo de documentos", alert=True)
        self.limpiar_documentos()
        self.mostrar_estantes()
        self.btnadd_doc.configure(state="disable")
        self.btneliminar_doc.configure(state="disable")

    def delete_doc_estante(self):
        #nombre_estante = self.combo_estantes_delete.get() # obtengo el nombre del estante del que voy a eliminar el libro
        estante = self.database_manager.selectEstanteByName(self.combo_estantes_delete.get())
        self.database_manager.deleteDocumentoEstante(self.doc_id_editar, estante.id)
        self.database_manager.updateEstanteSize(estante.id, estante.tamano-1)
        Messagebox.show_info(title="Éxito", message="Documento eliminado con éxito del estante")
        self.limpiar_documentos()
        self.mostrar_estantes()
        self.btnadd_doc.configure(state="disable")
        self.btneliminar_doc.configure(state="disable")

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
        self.limpiar_documentos()
        dato = self.tableviewDocs.view.item(self.tableviewDocs.view.selection())["values"]
        self.doc_id_editar = int(dato[0]) # id del libro 
        documento = self.database_manager.selectDocumentById(self.doc_id_editar) # obtengo el documento con ese id
        self.e_id.insert(0, self.doc_id_editar)
        self.e_titulo.insert(0, documento.titulo)
        if documento.formato_id == 1000:
            self.e_formato.insert(0, "Físico")
        else:
            self.e_formato.insert(0, "PDF")
        self.e_tipo_doc.insert(0, documento.tipo)
        # relleno los combobox con los respectivos estantes
        self.fill_estantes_add()
        self.fill_estantes_delete()
        self.btnadd_doc.configure(state="normal")
        self.btneliminar_doc.configure(state="normal")

    def limpiar_estantes(self):
        self.e_nombre.delete(0, END)
        self.e_tematica.delete(0, END)
        self.e_tipo.delete(0, END)
    
    def limpiar_documentos(self):
        self.e_id.delete(0, END)
        self.e_titulo.delete(0, END)
        self.e_formato.delete(0, END)
        self.combo_estantes_add.delete(0, END)    # probar esto tambien .set("")
        self.combo_estantes_delete.delete(0, END)

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

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def widgets(self):
        # FRAMES
        self.canvas = Canvas(self.principal)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(self.principal, orient=VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        frame = Frame(self.canvas)
        self.canvas.create_window((0,0), window=frame, anchor='nw')

        frame.bind("<Configure>", self.on_frame_configure)

        for estante in self.estantes:
            nombre_estante = estante.nombre
            tematica_estante = estante.tematica
            docs = self.database_manager.selectDocsEstante(estante.id) # obtengo los documentos de ese estante
            subframe = Frame(frame, bootstyle = INFO)
            subframe.pack(side = TOP, fill = BOTH, expand=True, padx=10)
            subframe.config(width=1220, height=400)
            subframe.pack_propagate(False)

            lblframe1 = Labelframe(subframe, text=f"Formulario del estante {nombre_estante}", bootstyle= PRIMARY)
            lblframe1.pack(side=TOP, fill=BOTH, expand=True)

            label_nombre = Label(lblframe1, text=f"Estante {nombre_estante}")
            label_nombre.place(x=500, y=5)

            label_tematica = Label(lblframe1, text=f"Temática: {tematica_estante}")
            label_tematica.place(x=700, y=5)

            # para cada documento del estante creo un marco para la portada y el nombre
            for index, doc in enumerate(docs):
                frame_doc = Frame(lblframe1)
                frame_doc.place(x=index*100, y=5, width=150, height=200)

                label_titulo_doc = Label(frame_doc, text=doc.titulo)
                label_titulo_doc.place(x=0, y=180)

        self.canvas.update_idletasks()

        """scrollbar = Scrollbar(frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)"""

        """frame = Frame(self)
        frame.pack(side = TOP, fill = BOTH, expand=True)"""

        #frame.config(yscrollcommand=scrollbar.set)
        #scrollbar.config(command=frame.yview)
        """ frame1 = Frame(frame, bootstyle= INFO)
            frame1.place(x=10, y=0, width=1200, height=200)

            lblframe1 = Labelframe(frame1, text=f"Formulario estante{i}", bootstyle= PRIMARY)
            lblframe1.pack(side=TOP, fill=BOTH, expand=True)

            self.btnpulsame = Button(lblframe1, text="Guardar", command="")
            self.btnpulsame.place(x=10, y=150, width=135)"""
        
        """self.canvas = Canvas()
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(self.principal, orient=VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        frame = Frame(self.canvas)
        self.canvas.create_window((0,0), window=frame, anchor='nw')

        frame.bind("<Configure>", self.on_frame_configure)"""


        

    