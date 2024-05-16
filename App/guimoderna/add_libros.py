from ttkbootstrap import *
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from tkinter import *
from persistence.repository.database_manager import DatabaseManager
from persistence.model import *
import re
import datetime
from datetime import *

from ttkbootstrap import * 
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox

class AddLibro(Frame):
    def __init__(self, id, master = None):
        super().__init__(master)
        #super().__init__(themename="superhero", size=(1260, 700), title="Interfaz moderna") #proporcion 1.8
        self.database_manager = DatabaseManager()
        self.user_id = id
        self.doc_id_editar = ""
        self.user: Usuario = self.database_manager.selectUserById(self.user_id)
        self.estantes = self.database_manager.selectAllEstantesByIdOwner(self.user_id)
        self.principal = master
        self.is_new = True
        self.widgets()
        self.mostrar()

    def entry_label(self,frame,x,y,texto):
        lbl = Label(frame, text=texto,bootstyle=PRIMARY)
        lbl.place(x=x,y=y)

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
        patron_fecha = r'^\d{4}-\d{2}-\d{2}$'
        if self.e_titulo.get() == "" or self.e_autor.get() == "" or self.e_formato.get() == "" or self.e_isbn.get() == "" or self.e_editorial.get() == "":
            Messagebox.show_error(title="Error", message="Faltan campos obligatorios", alert=True)
            return False
        elif len(self.e_titulo.get()) == 0:
            Messagebox.show_error(title="Error", message="El título es un campo obligatorio", alert=True)
            return False 
        elif not self.e_isbn.get().isdigit():
            Messagebox.show_error(title="Error", message="El ISBN tiene que ser un conjunto de dígitos", alert=True)
            return False
        elif not re.match(patron_fecha, self.e_fecha.get()):
            Messagebox.show_error(title="Error", message="La fecha no está en el formato adecuado", alert=True)
            return False
        return True

    def mostrar(self):
        formato = ""
        dato = []
        datosDocumentos = self.database_manager.selectAllDocumentosLibros(self.user_id) # obtengo los documentos que sean libros y pertenezcan al usuario
        if len(datosDocumentos) != 0:
            for documento in datosDocumentos:
                datosLibro = self.database_manager.selectLibroById(documento.id) # obtengo los datos del libro
                if documento.formato_id == 1000:
                    formato = "Físico"
                else:
                    formato = "PDF"
                fila = [documento.id, documento.titulo, documento.autor, documento.idioma, formato, datosLibro.isbn, datosLibro.editorial, datosLibro.tematica] # probar sino con datosLibro[0]
                dato.append(fila)
            #dato = [datosDocumentos[0],datosDocumentos[3],datosDocumentos[4],datosDocumentos[6],datosDocumentos[5],datosLibros[0],datosLibros[3],datosLibros[4]]
        self.tableview.build_table_data(self.coldata, dato)

    def guardar(self):
        if self.validar(): #validar datos de los campos antes de guardar
            documento = Documento()
            documento.titulo = self.e_titulo.get()
            documento.autor = self.e_autor.get()
            documento.idioma = self.e_idioma.get()
            #gestion de ids de formato
            if self.e_formato.get() == "físico":
                documento.formato = self.database_manager.selectFormatoByTipo("Físico")
            else:
                documento.formato = self.database_manager.selectFormatoByTipo("PDF")
            # hay que guardar sí o sí un entero para estante pero cuidado porque no si no hay estantes no puede haber enteros
            if self.e_estante.get() is None or self.e_estante.get() == "Ninguno":
                documento.estante = None
            else:
                est = self.database_manager.selectEstanteByName(self.e_estante.get())
                documento.estante = est.id
            documento.tipo = "Libro" #siempre va a ser libro
            documento.propietario_id = self.user_id

            if self.is_new: # si no es una actualización
                #añadimos el documento
                self.database_manager.insertDocumento(documento)
            libro = Libro()
            libro.isbn = self.e_isbn.get()
            libro.editorial = self.e_editorial.get()
            libro.fecha_publicacion = self.e_fecha.get()
            libro.tematica = self.e_tematica.get()
            libro.nombre_genero = self.e_genero.get()
            libro.nombre_categoria = self.e_categoria.get()
            libro.id_documento = self.database_manager.selectIdLastDocumento()
            libro.propietario_id = self.user_id
        #return Messagebox.show_error(title="Error",message="Ingresar un nombre válido para el producto", alert=True)
        
            if self.is_new: # si no es una actualización
                #añadimos el libro
                self.database_manager.insertLibro(libro)
                if not (self.e_estante.get() is None or self.e_estante.get() == "Ninguno"):
                    self.database_manager.insertDocumentoEstante(documento.id, documento.estante)
                Messagebox.show_info(title="Éxito", message="Datos guardados con éxito")
            else: # es una actualización
                valor = Messagebox.show_question(title="Alerta", message="¿Estás seguro de que deseas actualizar el libro?", alert=True)
                if valor == "Sí":
                    estante = ""
                    formato = ""
                    if len(self.estantes) == 0 or self.e_estante.get() is None:
                        estante = None
                    else:
                        estante = self.e_estante.get()
                    if self.e_formato.get() == "físico":
                        formato = 1000
                    else:
                        formato = 1001
                    self.database_manager.updateDocumento(self.doc_id_editar, self.e_titulo.get(), self.e_autor.get(), self.e_idioma.get(), formato, estante)
                    self.database_manager.updateLibro(self.doc_id_editar, self.e_isbn.get(), self.e_fecha.get(), self.e_editorial.get(), self.e_tematica.get(), self.e_genero.get(), self.e_categoria.get())
                    self.is_new = True
                    Messagebox.show_info(title="Éxito", message="Datos actualizados con éxito")
                self.btneditar.configure(state="disable")
                self.btneliminar.configure(state="disable")
            self.mostrar()
            self.limpiar()

    def limpiar(self):
        self.e_titulo.delete(0, END)
        self.e_autor.delete(0, END)
        self.e_idioma.delete(0, END)
        self.e_estante.current(0)
        self.e_isbn.delete(0,END)
        self.e_editorial.delete(0, END)
        self.e_fecha.delete(0,END)
        self.e_tematica.delete(0,END)
        self.e_genero.delete(0, END) # podría ser también .selection_clear()
        self.e_categoria.delete(0, END)
    
    def editar(self):
        self.is_new = False
        self.limpiar()
        dato = self.tableview.view.item(self.tableview.view.selection())["values"]
        self.doc_id_editar = int(dato[0]) # id del libro y documento a editar
        documento = self.database_manager.selectDocumentById(self.doc_id_editar)
        libro = self.database_manager.selectLibroById(self.doc_id_editar)
        self.e_titulo.insert(0, documento.titulo) # probar sino con documento[0]
        self.e_autor.insert(0, documento.autor) # probar sino con documento[0]
        self.e_idioma.insert(0, documento.idioma) # probar sino con documento[0]
        if documento.formato_id == 1000:
            self.e_formato.set("físico")
        else: 
            self.e_formato.set("pdf")
        self.e_isbn.insert(0, libro.isbn) # probar sino con libro[0]
        self.e_editorial.insert(0, libro.editorial) # probar sino con libro[0]
        self.e_fecha.insert(0, str(libro.fecha_publicacion)) # probar sino con libro[0]
        self.e_tematica.insert(0, libro.tematica) # probar sino con libro[0]
        self.e_genero.current(0)
        self.e_categoria.current(0)

    def eliminar(self):
        dato = self.tableview.view.item(self.tableview.view.selection())["values"]
        valor = Messagebox.show_question(title="Alertar", message="¿Estás seguro de que deseas eliminar este libro?", alert=True)
        if valor == "Sí": #se elimina
            self.database_manager.deleteLibroById(int(dato[0]))
            self.database_manager.deleteDocumentoById(int(dato[0]))
        Messagebox.show_info(title="Éxito", message="Libro eliminado con éxito")
        
        self.mostrar()
        self.btneditar.configure(state="disable")
        self.btneliminar.configure(state="disable")

    def eventos(self, event):
        print(self.tableview.view.item(self.tableview.view.selection())["values"])
        #if len(self.tableview.view.item(self.tableview.view.selection())["values"])!=0:
        self.btneditar.configure(state="normal")
        self.btneliminar.configure(state="normal")
            #print(self.tableview.view.item(self.tableview.view.selection())["values"])

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
        lbl = Label(lblframe1, text="Formato", bootstyle=PRIMARY)
        lbl.place(x=5,y=120)
        rb_formato1 = Radiobutton(lblframe1, text="Físico", variable=self.e_formato, value="físico")
        rb_formato1.place(x=105, y=120)
        rb_formato2 = Radiobutton(lblframe1, text="PDF", variable=self.e_formato, value="pdf")
        rb_formato2.place(x=200, y=120)
        # rellenamos el combobox de los estantes
        opciones_estantes=['Ninguno']
        for estante in self.estantes:
            opciones_estantes.append(estante.nombre)
        self.e_estante = self.comboboxea(lblframe1, 5, 160, "Estante", opciones_estantes)

        #campos de libro
        self.e_isbn = self.entry_label(lblframe1,5,200,"ISBN")
        self.e_editorial = self.entry_label(lblframe1,5,240,"Editorial")
        self.e_fecha = self.entry_label(lblframe1,5,280,"Fecha")
        self.e_tematica = self.entry_label(lblframe1,5,320,"Temática")
        opciones_genero = self.database_manager.selectGeneros()
        self.e_genero = self.comboboxea(lblframe1, 5, 360, "Género", opciones_genero)
        opciones_categoria = self.database_manager.selectCategorias()
        self.e_categoria = self.comboboxea(lblframe1, 5, 400, "Categoría", opciones_categoria)

        self.btnguardar = Button(lblframe1,text="Guardar", command=self.guardar)
        self.btnguardar.place(x=10,y=450,width=135)

        self.btneditar = Button(lblframe1,text="Editar", command=self.editar, bootstyle=SUCCESS)
        self.btneditar.configure(state= "disable")
        self.btneditar.place(x=10, y=490, width=135)

        self.btneliminar = Button(lblframe1, text="Eliminar", command=self.eliminar, bootstyle=DANGER)
        self.btneliminar.configure(state= "disable")
        self.btneliminar.place(x=10, y=530, width=135)

        # TABLA LBLFRAME2
        self.coldata = [
            {"text":"ID", "width":200},
            {"text":"Titulo", "stretch":True},
            {"text":"Autor", "width":200},
            {"text":"Idioma", "width":50},
            {"text":"Formato", "width":30},
            {"text":"ISBN", "width":100},
            {"text":"Editorial", "width":200},
            {"text":"Temática", "width":100},
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
    

    


    
        

    
        







