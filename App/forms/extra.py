class FormularioAddDocumento(Window):
    def __init__(self, panel_principal):
        self.frame_principal = panel_principal

        super().__init__(themename="superhero", size=(1260, 700), title="Interfaz moderna") #proporcion 1.8
        self.widgets()
        #Datos.crear()
        self.mostrar()
        self.idlibro = -1

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
        datosDocumentos = self.database_manager.selectAllDocumentos() # obtengo los documentos
        datosLibros = self.database_manager.selectAllLibros() # obtengo los libros
        dato = [datosDocumentos[0],datosDocumentos[3],datosDocumentos[4],datosDocumentos[6],datosDocumentos[5],datosLibros[0],datosLibros[3],datosLibros[4]]
        self.tableview.build_table_data(self.coldata,dato)
        
    def guardar(self):
        #validar() validar datos de los campos antes de guardar
        documento = Documento()
        documento.titulo = self.e_titulo.get()
        documento.autor = self.e_autor.get()
        documento.idioma = self.e_idioma.get()
        #gestion de ids de formato
        if self.e_formato.get() == "Físico":
            documento.formato = 1000
        else:
            documento.formato = 1001
        documento.estante = self.e_estante.get()
        documento.tipo = "Libro" #siempre va a ser libro

        libro = Libro()
        libro.isbn = self.e_isbn.get()
        libro.editorial = self.e_editorial.get()
        libro.fecha = self.e_fecha.get()
        libro.tematica = self.e_tematica.get()
        libro.nombre_genero = self.e_genero.get()
        libro.nombre_categoria = self.e_categoria.get()
        
        #return Messagebox.show_error(title="Error",message="Ingresar un nombre válido para el producto", alert=True)
        
        if self.idlibro == -1:
            #añadimos el documento
            self.database_manager.insertDocumento(documento)
            #añadimos el libro
            self.database_manager.insertLibro(libro)
            #Messagebox.show_error(tittle="Error",message="El libro ya esta registrado",alert=True)
        else:
            valor = Messagebox.show_question(title="Alerta",message="¿Estás seguro de que deseas actualizar el libro?",alert=True)
            if valor == "Sí":
                self.database_manager.insertDocumento(documento)
                self.database_manager.insertLibro(libro)
                #sql = "UPDATE libros SET titulo = ?, autor = ?, idioma = ?, editorial = ? WHERE id = ?"
                #parametros = (titulo,autor,idioma,editorial,self.idlibro)
                #Datos.guardar(sql,parametros)
                self.idlibro = -1
        self.mostrar()
        self.limpiar()
        self.btneditar.configure(state="disable")
        self.btneliminar.configure(state="disable")

    def limpiar(self):
        self.e_titulo.delete(0, END)
        self.e_autor.delete(0, END)
        self.e_idioma.delete(0, END)
        self.e_estante.delete(0,END)
        self.e_isbn.delete(0,END)
        self.e_editorial.delete(0, END)
        self.e_fecha.delete(0,END)
        self.e_tematica.delete(0,END)
        self.e_genero.delete(0,END)
        self.e_categoria.delete(0,END)

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
            #Datos.guardar("DELETE FROM libros WHERE id = ?",(dato,))
            pass
        self.mostrar()
        self.btneditar.configure(state="disable")
        self.btneliminar.configure(state="disable")


    def eventos(self,event):
        #if len(self.tableview.view.item(self.tableview.view.selection())["values"])!=0:
        self.btneditar.configure(state="normal")
        self.btneliminar.configure(state="normal")
            #print(self.tableview.view.item(self.tableview.view.selection())["values"])
        

    def widgets(self):
        #frame =Frame(self)
        self.frame_principal.pack(side = TOP, fill = BOTH, expand=True)
        frame1 = Frame(self.frame_principal, bootstyle= INFO)
        frame1.place(x=5,y=0,width=410,height=690)

        lblframe1 = Labelframe(frame1,text="Formulario",bootstyle= PRIMARY)
        lblframe1.pack(side=TOP, fill=BOTH, expand=True)

        # FORMULARIO
        #campos de documento
        self.e_titulo = self.entry_label(lblframe1,5,0,"Título")
        self.e_autor = self.entry_label(lblframe1,5,40,"Autor")
        self.e_idioma = self.entry_label(lblframe1,5,80,"Idioma")
        opciones_formato = ["Físico", "PDF"]
        self.e_formato = self.comboboxea(lblframe1,5,120,"Formato",opciones_formato)
        opciones_estante = ["estante1", "estante2"] #habrá que rellenar 
        self.e_estante = self.comboboxea(lblframe1,5,160,"Estante",opciones_estante)

        #campos de libro
        self.e_isbn = self.entry_label(lblframe1,5,200,"ISBN")
        self.e_editorial = self.entry_label(lblframe1,5,240,"Editorial")
        self.e_fecha = self.entry_label(lblframe1,5,280,"Fecha")
        self.e_tematica = self.entry_label(lblframe1,5,320,"Temática")
        opciones_genero = ["No ficción", "Fantasía", "Ciencia ficción"] #habrá que rellenar 
        self.e_genero = self.comboboxea(lblframe1,5,360,"Género",opciones_genero)
        opciones_categoria = ["estante1", "estante2"] #habrá que rellenar 
        self.e_categoria = self.comboboxea(lblframe1,5,400,"Categoría",opciones_categoria)

        btnguardar = Button(lblframe1,text="Guardar",command=self.guardar)
        btnguardar.place(x=105,y=440,width=135)

        self.btneditar = Button(lblframe1,text="Editar",command=self.editar,bootstyle=SUCCESS)
        self.btneditar.configure(state= "disable")
        self.btneditar.place(x=10,y=480,width=200)

        self.btneliminar = Button(lblframe1,text="Eliminar",command=self.eliminar,bootstyle=DANGER)
        self.btneliminar.configure(state= "disable")
        self.btneliminar.place(x=10,y=520,width=200)

        #VISUALIZACIÓN - TABLA
        frame2 = Frame(self.frame_principal, bootstyle=DANGER)
        frame2.place(x=420,y=0,width=830,height=690)

        lblframe2 = LabelFrame(frame2, text="Datos",bootstyle= SUCCESS)
        lblframe2.pack(side=TOP, fill=BOTH, expand=True)
        self.coldata = [
            {"text":"ID","width":20},
            {"text":"Titulo","width":200},
            {"text":"Autor","width":50},
            {"text":"Idioma","stretch":True},
            {"text":"Formato","width":30},
            {"text":"ISBN","width":50},
            {"text":"Editorial","width":200},
            {"text":"Temática","width":50},
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
        self.tableview.view.bind("<Double-1>",self.eventos) #Button-1
        self.tableview.align_column_center()