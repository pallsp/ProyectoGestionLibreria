from ttkbootstrap import * 
from add_libros import AddLibro
from add_otros import AddOtro
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.dialogs import Messagebox
from persistence.model import *
from persistence.repository.database_manager import DatabaseManager
import re 
from datetime import datetime
import requests 
from io import BytesIO
import util.generic as utl_img

class VerBiblioteca(Frame):
    def __init__(self, id, master = None):
        super().__init__(master)
        self.database_manager = DatabaseManager()
        self.user_id = id
        self.estantes = self.database_manager.selectAllEstantesByIdOwner(self.user_id)
        self.principal = master
        self.empty_image = ImageTk.PhotoImage(Image.new('RGBA', (120, 200), (255, 255, 255, 0)))
        self.tk_images = [] # lista para mantener las referencias de las imágenes
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
        pass

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
        pass

    def seleccionar(self):
        pass

    def limpiar(self):
        self.label_img.config(image=self.empty_image)
        self.e_titulo.delete(0, END)
        self.e_autor.delete(0, END)
        self.e_idioma.delete(0, END)
        self.e_fecha.delete(0, END)
        self.e_isbn.delete(0, END)
        self.e_editorial.delete(0, END)
        self.e_tematica.delete(0, END)
        self.e_emisor.delete(0, END)
        self.e_tipo.delete(0, END)
        self.btnlimpiar.configure(state="disabled")

    def editar(self):
        pass

    def eliminar(self):
        pass

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # OBTENER DE API
    def fetch_book_cover(self, isbn):
        url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg?default=false"
        response = requests.get(url)
        if response.status_code == 200: 
            image_data = response.content
            return Image.open(BytesIO(image_data))
        elif response.status_code == 404:
            print("Imagen no encontrada")
            return None
        else:
            raise Exception("No se pudo recuperar la imagen de la portada")

    # TRASLADAR DATOS
    def move_data(self, doc:Documento):
        self.limpiar()
        self.e_titulo.insert(0, doc.titulo)
        self.e_autor.insert(0, doc.autor)
        self.e_idioma.insert(0, doc.idioma)
        if doc.tipo == "Libro":
            libro = self.database_manager.selectLibroById(doc.id)
            self.e_fecha.insert(0, libro.fecha_publicacion)
            self.e_isbn.insert(0, libro.isbn)
            self.e_editorial.insert(0, libro.editorial)
            self.e_tematica.insert(0, libro.tematica)
            self.set_cover(libro.isbn)
        else:
            otro = self.database_manager.selectOtroById(doc.id)
            self.e_fecha.insert(0, otro.fecha)
            self.e_emisor.insert(0, otro.emisor)
            self.e_tipo.insert(0, otro.tipo)
            image = utl_img.leer_imagen("/home/pablo/PROYECTO/imagenes/notfound.jpg", (120, 200))
            self.tk_images.append(image)
            self.label_img = tk.Label(self.frame_img, image=image)
            self.label_img.place(x=5, y=0)  
        self.btnlimpiar.configure(state= "normal")

    def set_cover(self, isbn):
        try:
            image = self.fetch_book_cover(isbn) #8420674265 para probar
            if image:
                res_image = image.resize((120,200), Image.LANCZOS)
                tk_image = ImageTk.PhotoImage(res_image) # size=(150, 250)
                self.tk_images.append(tk_image)
                self.label_img = tk.Label(self.frame_img, image=tk_image)
                self.label_img.place(x=5, y=0)
            else:
                image = utl_img.leer_imagen("/home/pablo/PROYECTO/imagenes/notfound.jpg", (120, 200))
                self.tk_images.append(image)
                self.label_img = tk.Label(self.frame_img, image=image)
                self.label_img.place(x=5, y=0)
        except Exception as error: 
            print(f"Error al configurar la portada del libro: {error}")
            image = utl_img.leer_imagen("/home/pablo/PROYECTO/imagenes/notfound.jpg", (120, 200))
            self.tk_images.append(image)
            self.label_img = tk.Label(self.frame_img, image=image)
            self.label_img.place(x=5, y=0)

    def mostrar(self):
        formato = ""
        dato = []
        datosDocumentos = self.database_manager.selectAllDocumentosLibros(self.user_id) # obtengo los documentos que pertenezcan al usuario y sean PDF 
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

    def widgets(self):
        font_awesome = font.Font(family='FontAwesome', size=12)
        # FRAMES
        frame = Frame(self)
        frame.pack(side = TOP, fill = BOTH, expand=True)

        frame1 = Frame(frame, bootstyle= INFO)
        frame1.place(x=10, y=0, width=880, height=680)

        lblframe1 = Labelframe(frame1, text="Estantes", bootstyle= PRIMARY)
        lblframe1.pack(side=TOP, fill=BOTH, expand=True)

        frame2 = Frame(frame, bootstyle=DANGER)
        frame2.place(x=900, y=0, width=350, height=680)

        lblframe2 = LabelFrame(frame2, text="Datos", bootstyle=SUCCESS)
        lblframe2.pack(side=TOP, fill=BOTH, expand=True)

        self.canvas = Canvas(lblframe1)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        scrollbar = Scrollbar(lblframe1, orient=VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        otro_frame = Frame(self.canvas)
        self.canvas.create_window((0,0), window=otro_frame, anchor='nw')

        otro_frame.bind("<Configure>", self.on_frame_configure)

        for estante in self.estantes:
            nombre_estante = estante.nombre
            tematica_estante = estante.tematica
            docs = self.database_manager.selectDocsEstante(estante.id) # obtengo los documentos de ese estante
            altura = 300*(len(docs)//3+1)
            subframe = Frame(otro_frame, bootstyle = INFO)
            subframe.pack(side = TOP, fill = BOTH, expand=True, padx=10)
            subframe.config(width=850, height=altura)
            subframe.pack_propagate(False)

            otro_lblframe = Labelframe(subframe, text=f"Estante {nombre_estante}", bootstyle= PRIMARY)
            otro_lblframe.pack(side=TOP, fill=BOTH, expand=True)

            label_nombre = Label(otro_lblframe, text=f"Estante: {nombre_estante}")
            label_nombre.place(x=200, y=5)

            label_tematica = Label(otro_lblframe, text=f"Temática: {tematica_estante}")
            label_tematica.place(x=400, y=5)
            frames_doc = []
            botones = []
            for index, doc in enumerate(docs):
                i = index % 3
                j = index//3 + 1
                if j > 1:
                    j+=2
                frame_doc = Labelframe(otro_lblframe, text=doc.tipo, bootstyle=DANGER)
                frame_doc.place(x=(i*200)+25, y=50*j, width=200, height=120)

                label_titulo_doc = Label(frame_doc, text=doc.titulo)
                label_titulo_doc.place(x=5, y=5, width=150)

                label_autor_doc = Label(frame_doc, text=doc.autor)
                label_autor_doc.place(x=5, y=35, width=150)

                btnmove = tk.Button(frame_doc, text="\u2192", font=font_awesome, command=lambda d=doc: self.move_data(d), bd=0, bg="#df5553", fg="white")
                btnmove.place(x=5, y=70, width=20, height=20)

                botones.append(btnmove)
                frames_doc.append(frame_doc)
                if doc.tipo == "Libro":
                    pass
                else: 
                    pass
                
            #image = self.fetch_book_cover(8420674265)
            #image.resize((60,100), Image.LANCZOS)
            #tk_image = ImageTk.PhotoImage(image) # size=(150, 250)
            #self.tk_images.append(tk_image)
            #label = tk.Label(lblframe1, image=tk_image)
            #label.place(x=0, y=100)

        self.canvas.update_idletasks()
        # marco para la imagen 
        self.frame_img = Labelframe(lblframe2, text="Portada", bootstyle=LIGHT)
        self.frame_img.place(x=110, y=5, width=130, height=225)

        self.label_img = tk.Label(self.frame_img, image=None)
        self.label_img.place(x=5, y=0)
        # campos generales de documento
        self.e_titulo = self.entry_label(lblframe2, 5, 240, "Título")
        self.e_autor = self.entry_label(lblframe2, 5, 280, "Autor")
        self.e_idioma = self.entry_label(lblframe2, 5, 320, "Idioma")
        self.e_fecha = self.entry_label(lblframe2, 5, 440, "Fecha")
        # campos propios de libro
        self.e_isbn = self.entry_label(lblframe2, 5, 360, "ISBN")
        self.e_editorial = self.entry_label(lblframe2, 5, 400, "Editorial")
        self.e_tematica = self.entry_label(lblframe2, 5, 480, "Temática")
        # campos propios de otro
        self.e_emisor = self.entry_label(lblframe2, 5, 520, "Emisor")
        self.e_tipo = self.entry_label(lblframe2, 5, 560, "Tipo")
        #self.e_subtipo = self.entry_label(lblframe2, 5, 600, "Subtipo")

        self.btnlimpiar = Button(lblframe2, text="Limpiar", command=self.limpiar, bootstyle=SUCCESS)
        self.btnlimpiar.configure(state= "disabled")
        self.btnlimpiar.place(x=120, y=615, width=135)


        

    