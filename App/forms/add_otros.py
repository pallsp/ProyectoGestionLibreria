from ttkbootstrap import *
from ttkbootstrap import *
import tkinter as tk
from tkinter import ttk 
from tkinter import *
from persistence.repository.database_manager import DatabaseManager
from persistence.model import *
import re
import datetime
from datetime import *

from ttkbootstrap import * 
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox

from ttkbootstrap import * 
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox

class AddOtro(Frame):
    def __init__(self, id, master = None):
        super().__init__(master)
        self.opciones_subtipo = ["Apuntes", "Factura", "Impreso", "Billetes"]
        self.database_manager = DatabaseManager()
        self.user_id = id
        self.doc_id_editar = ""
        self.estantes = self.database_manager.selectAllEstantesByIdOwner(self.user_id)
        self.principal = master
        self.is_new = True
        self.widgets()
        self.mostrar()
    
    def entry_label(self, frame, x, y, texto):
        lbl = Label(frame, text=texto, bootstyle=PRIMARY)
        lbl.place(x=x,y=y)

        entry = Entry(frame, bootstyle=(PRIMARY))
        entry.place(x=x+100,y=y)
        return entry

    def comboboxea(self, frame, x, y, texto, opciones):
        lbl = Label(frame, text=texto, bootstyle=PRIMARY)
        lbl.place(x=x,y=y)

        combo = Combobox(frame, values=opciones)
        if len(opciones) != 0:
            combo.current(0)
        combo.place(x=x+100, y=y)
        return combo

    def validar(self):
        patron_fecha = r'^\d{4}-\d{2}-\d{2}$'
        if not(self.e_estante.get() == "" or self.e_estante.get() == "Ninguno"):
            est = self.database_manager.selectEstanteByName(self.e_estante.get())
            if est.tipo == "LIBRO":
                Messagebox.show_error(title="Error", message="No se puede agregar el libro a este estante", alert=True)
                return False
        if self.e_titulo.get() == "" or self.e_autor.get() == "" or self.e_formato.get() == "" or self.e_tipo.get() == "" or self.e_subtipo.get() == "":
            Messagebox.show_error(title="Error", message="Faltan campos obligatorios", alert=True)
            return False
        elif len(self.e_titulo.get()) == 0:
            Messagebox.show_error(title="Error", message="El título es un campo obligatorio", alert=True)
            return False 
        elif not re.match(patron_fecha, self.e_fecha.get()):
            Messagebox.show_error(title="Error", message="La fecha no está en el formato adecuado", alert=True)
            return False
        else:
            try:
                # Intentar convertir la fecha en un objeto datetime
                datetime.strptime(self.e_fecha.get(), '%Y-%m-%d')
            except ValueError:
                Messagebox.show_error(title="Error", message="La fecha no es válida", alert=True)
                return False
        return True

    def mostrar(self):
        formato = ""
        dato = []
        datosDocumentos = self.database_manager.selectAllDocumentosOtros(self.user_id) # obtengo los documentos que sean otros y pertenezcan al usuario
        if len(datosDocumentos) != 0:
            for documento in datosDocumentos:
                if documento.formato_id == 1000:
                    formato = "Físico"
                else:
                    formato = "PDF"
                datosOtro = self.database_manager.selectOtroById(documento.id) # obtengo los datos del libro
                fila = [documento.id, documento.titulo, documento.autor, documento.idioma, formato, datosOtro.emisor, datosOtro.tipo, datosOtro.subtipo] # probar sino con datosOtro[0]
                dato.append(fila)
        self.tableview.build_table_data(self.coldata,dato)

    def guardar(self):
        if self.validar(): #validar datos de los campos antes de guardar
            estante_d = ""
            id_d = ""
            biblioteca = self.database_manager.selectBiblioteca(self.user_id)
            documento = Documento()
            documento.titulo = self.e_titulo.get()
            documento.autor = self.e_autor.get()
            documento.idioma = self.e_idioma.get()
            #gestion de ids de formato
            if self.e_formato.get() == "físico":
                documento.formato = self.database_manager.selectFormatoByTipo("Físico")
            else:
                documento.formato = self.database_manager.selectFormatoByTipo("PDF")
            # hay que guardar sí o sí un entero para estante
            if len(self.estantes) == 0 or self.e_estante.get() == "" or self.e_estante.get() == "Ninguno":
                documento.estante = None
                estante_d = None
            else:
                est = self.database_manager.selectEstanteByName(self.e_estante.get())
                documento.estante = est.id
                estante_d = est.id
                self.database_manager.updateEstanteSize(est.id, est.tamano+1)
            documento.tipo = "Otro" #siempre va a ser otro
            documento.propietario_id = self.user_id
            documento.biblioteca_id = biblioteca.id
            
            if self.is_new: # si no es una actualización
                #añadimos el documento
                self.database_manager.insertDocumento(documento)
            otro = Otro()
            otro.emisor = self.e_emisor.get()
            otro.fecha = self.e_fecha.get()
            otro.tipo = self.e_tipo.get()
            otro.subtipo = self.e_subtipo.get()
            otro.id_documento = self.database_manager.selectIdLastDocumento()
            otro.propietario_id = self.user_id
            
            id_d = otro.id_documento
            if self.is_new: # si no es una actualización
                #añadimos el otro
                self.database_manager.insertOtro(otro)
                if not (self.e_estante.get() == "" or self.e_estante.get() == "Ninguno"):
                    self.database_manager.insertDocumentoEstante(id_d, estante_d)
                Messagebox.show_info(title="Éxito", message="Datos guardados con éxito")
            else: # es una actualización
                valor = Messagebox.show_question(title="Alerta", message="¿Estás seguro de que deseas actualizar el documento otro?", alert=True)
                if valor == "Sí":
                    estante_d = ""
                    formato = ""
                    if len(self.estantes) == 0 or self.e_estante.get() == "" or self.e_estante =="Ninguno":
                        estante_d = None
                    else:
                        est = self.database_manager.selectEstanteByName(self.e_estante.get())
                        if est not in self.database_manager.selectEstantesLibro(self.doc_id_editar):
                            self.database_manager.updateEstanteSize(est.id, est.tamano+1) 
                        documento.estante = est.id
                        estante_d = est.id
                    if self.e_formato.get() == "físico":
                        formato = 1000
                    else:
                        formato = 1001
                    self.database_manager.updateDocumento(self.doc_id_editar, self.e_titulo.get(), self.e_autor.get(), self.e_idioma.get(), formato, estante_d)
                    self.database_manager.updateOtro(self.doc_id_editar, self.e_emisor.get(), self.e_fecha.get(), self.e_tipo.get(), self.e_subtipo.get())
                    self.is_new = True
                    Messagebox.show_info(title="Éxito", message="Datos actualizados con éxito")
                self.btneditar.configure(state="disable")
                self.btneliminar.configure(state="disable")
            self.mostrar()
            self.limpiar()
            
    def limpiar_descartar(self):
        self.limpiar()
        self.btneditar.config(state="disabled")
        self.btneliminar.config(state="disabled")
        
    def limpiar(self):
        self.e_titulo.delete(0, END)
        self.e_autor.delete(0, END)
        self.e_idioma.delete(0, END)
        self.e_estante.delete(0,END)
        self.e_emisor.delete(0, END)
        self.e_fecha.delete(0, END)
        self.e_tipo.delete(0, END)
        self.e_subtipo.delete(0, END)
    
    def editar(self):
        self.is_new = False
        self.limpiar()
        dato = self.tableview.view.item(self.tableview.view.selection())["values"]
        self.doc_id_editar = int(dato[0]) # id del otro y documento a editar
        documento = self.database_manager.selectDocumentById(self.doc_id_editar)
        otro = self.database_manager.selectOtroById(self.doc_id_editar)
        self.e_titulo.insert(0, documento.titulo) # probar sino con documento[0]
        self.e_autor.insert(0, documento.autor)
        self.e_idioma.insert(0, documento.idioma)
        if documento.formato_id == 1000:
            self.e_formato.set("físico")
        else: 
            self.e_formato.set("pdf")
        self.e_emisor.insert(0, otro.emisor) # probar sino con otro[0]
        self.e_fecha.insert(0, str(otro.fecha))
        self.e_tipo.insert(0, otro.tipo)
        self.e_subtipo.current(0)
        self.btneliminar.configure(state="normal")

    def eliminar(self):
        dato = self.tableview.view.item(self.tableview.view.selection())["values"]
        valor = Messagebox.show_question(title="Alertar", message="¿Estás seguro de que deseas eliminar este otro?", alert=True)
        if valor == "Sí": #se elimina
            ests = self.database_manager.selectEstantesLibro(int(dato[0]))
            self.database_manager.deleteDocumentoDeEstantes(int(dato[0]))
            self.database_manager.deleteOtroById(int(dato[0]))
            self.database_manager.deleteDocumentoById(int(dato[0]))
            for est in ests: 
                self.database_manager.updateEstanteSize(est.id, est.tamano-1)
        Messagebox.show_info(title="Éxito", message="Otro eliminado con éxito")
        
        self.mostrar()
        self.btneditar.configure(state="disable")
        self.btneliminar.configure(state="disable")

    def eventos(self, event):
        print(self.tableview.view.item(self.tableview.view.selection())["values"])
        self.btneditar.configure(state="normal")

    def widgets(self):
        # FRAMES
        frame = Frame(self)
        frame.pack(side = TOP, fill = BOTH, expand=True)

        frame1 = Frame(frame, bootstyle= INFO)
        frame1.place(x=10, y=0, width=350, height=650)

        lblframe1 = Labelframe(frame1, text="Formulario", bootstyle= PRIMARY)
        lblframe1.pack(side=TOP, fill=BOTH, expand=True)

        frame2 = Frame(frame, bootstyle=DANGER)
        frame2.place(x=370, y=0, width=880, height=650)

        lblframe2 = LabelFrame(frame2, text="Datos", bootstyle=SUCCESS)
        lblframe2.pack(side=TOP, fill=BOTH, expand=True)

        # FORMULARIO LBLFRAME1
        #campos de documento
        self.e_titulo = self.entry_label(lblframe1,5,0,"Título")
        self.e_autor = self.entry_label(lblframe1,5,40,"Autor")
        self.e_idioma = self.entry_label(lblframe1,5,80,"Idioma")
        #opciones_formato = ["Físico", "PDF"]
        #self.e_formato = self.comboboxea(lblframe1,5,120,"Formato",opciones_formato)
        self.e_formato = StringVar()
        lbl = Label(lblframe1, text="Formato",bootstyle=PRIMARY)
        lbl.place(x=5,y=120)
        rb_formato1 = Radiobutton(lblframe1, text="Físico", variable=self.e_formato, value="físico")
        rb_formato1.place(x=105, y=120)
        rb_formato2 = Radiobutton(lblframe1, text="PDF", variable=self.e_formato, value="pdf")
        rb_formato2.place(x=200, y=120)
        # rellenamos el combobox de los estantes
        self.opciones_estantes=['Ninguno']
        for estante in self.estantes:
            if estante.tipo != "LIBRO":
                self.opciones_estantes.append(estante.nombre)
        self.e_estante = self.comboboxea(lblframe1, 5, 160, "Estante", self.opciones_estantes)

        #campos de otro
        self.e_emisor = self.entry_label(lblframe1, 5, 240, "Emisor")
        self.e_fecha = self.entry_label(lblframe1, 5, 280, "Fecha")
        self.e_tipo = self.entry_label(lblframe1, 5, 320, "Tipo")
        self.e_subtipo = self.comboboxea(lblframe1, 5, 360, "Subtipo", self.opciones_subtipo)

        self.btnguardar = Button(lblframe1, text="Guardar", command=self.guardar)
        self.btnguardar.place(x=10, y=480, width=135)

        self.btneditar = Button(lblframe1,text="Editar", command=self.editar, bootstyle=SUCCESS)
        self.btneditar.configure(state= "disable")
        self.btneditar.place(x=10, y=550, width=135)

        self.btneliminar = Button(lblframe1, text="Eliminar", command=self.eliminar, bootstyle=DANGER)
        self.btneliminar.configure(state= "disable")
        self.btneliminar.place(x=165, y=550, width=135)
        
        self.btnlimpiar = Button(lblframe1, text="Limpiar", command=self.limpiar_descartar, bootstyle=SUCCESS)
        self.btnlimpiar.place(x=165, y=480, width=135)

        # TABLA LBLFRAME2
        self.coldata = [
            {"text":"ID","width":200},
            {"text":"Titulo","stretch":True},
            {"text":"Autor","width":200},
            {"text": "Idioma", "width":50},
            {"text": "Formato", "width":30},
            {"text": "Emisor", "width":100},
            {"text":"Tipo","width":200},
            {"text":"Subtipo","width":100},
        ]
        self.tableview = Tableview(lblframe2, 
                              paginated=True,
                              searchable=True,
                              bootstyle=(SUCCESS),
                              stripecolor=("snow", "black"), #"cyan", None
                              autoalign=True,
                              autofit=True,
                              height=15,
                              delimiter=";")
        self.tableview.pack(fill=BOTH, expand=True,padx=5,pady=5)
        self.tableview.view.bind("<Double-1>",self.eventos)
        self.tableview.align_column_center()

