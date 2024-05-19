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
from tkinter import filedialog
from PIL import Image, ImageTk
from pdf2image import convert_from_path

class VisorPDF(Frame):
    def __init__(self, id, master = None):
        super().__init__(master)
        self.database_manager = DatabaseManager()
        self.user_id = id
        self.estantes = self.database_manager.selectAllEstantesByIdOwner(self.user_id)
        self.pages = ""
        self.total_pages = 0
        self.current_page = 0
        self.file_path = ""
        self.principal = master
        self.tk_images = [] # lista para mantener las referencias de las imágenes
        self.widgets()
        self.mostrar()
    
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

    def mostrar(self):
        datos = []
        datosDocumentos = self.database_manager.selectAllDocumentosPDF(self.user_id) # obtengo todos los documentos que sean PDF y pertenezcan al usuario
        if len(datosDocumentos) != 0:
            for documento in datosDocumentos:
                fila = [documento.id, documento.titulo, documento.autor, documento.idioma, documento.tipo]
                datos.append(fila)
        self.tableview.build_table_data(self.coldata, datos)

    def guardar(self):
        pass

    def seleccionar(self):
        pass

    def limpiar(self):
        self.label_img.config(image=None)
        self.e_titulo.delete(0, END)
        self.e_autor.delete(0, END)
        self.e_idioma.delete(0, END)
        self.e_fecha.delete(0, END)
        self.e_isbn.delete(0, END)
        self.e_editorial.delete(0, END)
        self.e_tematica.delete(0, END)
        self.e_emisor.delete(0, END)
        self.e_tipo.delete(0, END)
        self.e_subtipo.delete(0, END)

    def editar(self):
        pass

    def eliminar(self):
        pass

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def fetch_book_cover(self, isbn):
        url = f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
        response = requests.get(url)

        if response.status_code == 200: 
            image_data = response.content
            return Image.open(BytesIO(image_data))
        else:
            raise Exception("No se pudo recuperar la imagen de la portada")

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
            self.e_subtipo.insert(0, otro.subtipo)
            image = utl_img.leer_imagen("/home/pablo/PROYECTO/imagenes/notfound.jpg", (120, 200))
            self.tk_images.append(image)
            self.label_img = tk.Label(self.frame_img, image=image)
            self.label_img.place(x=5, y=0)  

    def eventos(self, event):
        print(self.tableview.view.item(self.tableview.view.selection())["values"])
        #self.btneditar.configure(state="normal")
        #self.btneliminar.configure(state="normal")

    def open_file_dialog(self):
        self.file_path = filedialog.askopenfilename(title="Elige un archivo PDF", filetypes=[('PDF files', '*.pdf')])
        if self.file_path:
            print("Archivo seleccionado: ", self.file_path)
            #self.set_image_perfil(self.file_path)
            #self.set_image_frame()
            self.btnviewfile.config(state="normal")
        
    def open_visor_file(self):
        self.btn_nextpage.config(state="normal")
        self.btn_prevpage.config(state="normal")
        self.btn_salir.config(state="normal")
        #pages = convert_from_path(self.file_path, first_page=1, last_page=2)
        self.pages = convert_from_path(self.file_path) # convierto mi archivo a páginas
        self.total_pages = len(self.pages)
        if self.pages:
            self.display_page()

    def display_page(self):
        img = self.pages[self.current_page]
        #img = img.resize((self.lblframe2.winfo_width(), self.lblframe2.winfo_height()), Image.LANCZOS)
        img = img.resize((540, 640), Image.LANCZOS) 
        img_tk = ImageTk.PhotoImage(img)

        self.label_page = Label(self.lblframe3, image=img_tk)
        self.label_page.image = img_tk  # Necesario para evitar que la imagen sea recolectada por el garbage collector
        #label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.label_page.place(x=0, y=0)

    def next_page(self):
        if self.current_page < self.total_pages-1:
            self.current_page += 1
            #self.label_page.forget() # eliminamos la actual página
            self.label_page.destroy()
            self.display_page()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            #self.label_page.forget() # eliminamos la actual página
            self.label_page.destroy()
            self.display_page()

    def exit_visor(self):
        #self.label_page.place_forget()
        self.label_page.destroy()
        self.btn_nextpage.config(state="disabled")
        self.btn_prevpage.config(state="disabled")
        self.btn_salir.config(state="disabled")
        self.file_path = ""
        self.total_pages = 0
        self.current_page = 0
        self.pages = ""
        

    def widgets(self):
        font_awesome = font.Font(family='FontAwesome', size=12)
        # FRAMES
        self.frame = Frame(self)
        self.frame.pack(side = TOP, fill = BOTH, expand=True)

        self.frame1 = Frame(self.frame, bootstyle= INFO)
        self.frame1.place(x=10, y=0, width=360, height=680)

        self.lblframe1 = Labelframe(self.frame1, text="Documentos", bootstyle= PRIMARY)
        self.lblframe1.pack(side=TOP, fill=BOTH, expand=True)

        self.frame2 = Frame(self.frame, bootstyle=DANGER)
        self.frame2.place(x=380, y=0, width=860, height=680)

        self.lblframe2 = LabelFrame(self.frame2, text="Visor", bootstyle=SUCCESS)
        self.lblframe2.pack(side=TOP, fill=BOTH, expand=True)

        self.lblframe3 = LabelFrame(self.lblframe2, text="PDF", bootstyle=DANGER)
        self.lblframe3.place(x=300, y=0, width=540, height=650)

        self.btn_nextpage = Button(self.lblframe2, text="Página anterior", command=self.prev_page)
        self.btn_nextpage.place(x=5, y=550, width=130)
        self.btn_nextpage.config(state="disabled")

        self.btn_prevpage = Button(self.lblframe2, text="Página siguiente", command=self.next_page)
        self.btn_prevpage.place(x=145, y=550, width=130)
        self.btn_prevpage.config(state="disabled")

        self.btn_salir = Button(self.lblframe2, text="Salir", command=self.exit_visor, bootstyle = DANGER)
        self.btn_salir.place(x=75, y=590, width=120)
        self.btn_salir.config(state="disabled")
        # TABLA DOCUMENTOS DE TIPO PDF LBLFRAME1
        self.coldata = [
            {"text":"ID", "width":200},
            {"text":"Titulo", "stretch":True},
            {"text":"Autor", "width":200},
            {"text":"Idioma", "width":50},
            {"text":"Tipo", "width":50}
        ]
        self.tableview = Tableview(self.lblframe1, 
                              paginated=True,
                              searchable=True,
                              bootstyle=(SUCCESS),
                              stripecolor=("snow", "black"), #"cyan", None
                              autoalign=True,
                              autofit=True,
                              height=15,
                              delimiter=";")
        #self.tableview.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.tableview.place(x=5, y=5, width=350, height=350)
        self.tableview.view.bind("<Double-1>", self.eventos)
        self.tableview.align_column_center()

        # ETIQUETAS Y SELECCIONAR PATH
        self.e_titulo = self.entry_label(self.lblframe1, 5, 400, "Título")
        self.e_autor = self.entry_label(self.lblframe1, 5, 440, "Autor")

        self.btnselfile = Button(self.lblframe1, text="Elegir archivo", command=self.open_file_dialog)
        self.btnselfile.place(x=105, y=500, width=130)

        self.btnviewfile = tk.Button(self.lblframe1, text="\u2192", font=font_awesome, command=self.open_visor_file, bd=0, bg="#df5553", fg="white") #command=lambda d=doc: self.move_data(d)
        self.btnviewfile.place(x=105, y=580, width=20, height=20)
        self.btnviewfile.config(state="disabled")

        """self.e_titulo.insert(0, doc.titulo)
        self.e_autor.insert(0, doc.autor)
        self.e_idioma.insert(0, doc.idioma)"""
        

        

    