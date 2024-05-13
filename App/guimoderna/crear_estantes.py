from ttkbootstrap import * 
from add_libros import AddLibro
from add_otros import AddOtro
from ttkbootstrap.dialogs import Messagebox

class AddEstantes(Frame):
    def __init__(self, id, lista_estantes: list, master = None):
        super().__init__(master)
        self.user_id = id
        self.estantes = lista_estantes
        self.principal = master
        self.widgets()
    
    def widgets(self):
        # BOTONES CENTRALES
        #font_botones = font.Font(family= "Times", size= 20, weight= "bold")
        btnlibros = Button(self.principal,text="LIBRO", bootstyle = SUCCESS, command=self.add_libro)
        #btnlibros.config(font=("Times", 20))
        btnlibros.place(x=300, y=300, width=200, height=150)

        btnotro = Button(self.principal,text="OTRO", bootstyle = DANGER, command=self.add_otro)
        #btnotro.config(font=("Times", 20))
        btnotro.place(x=520, y=300, width=200, height=150)

    def limpiar_pantalla(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()

    def add_libro(self):
        self.show_text_entry_dialog()
        self.limpiar_pantalla(self.principal)
        pantalla_documentos = AddLibro(self.user_id, self.estantes, self.principal)
        pantalla_documentos.place(x=0, y=0, width=1260, height=710)

    def add_otro(self):
        self.limpiar_pantalla(self.user_id, self.estantes, self.principal)
        pantalla_documentos = AddOtro(self.principal)
        pantalla_documentos.place(x=0, y=0, width=1260, height=710)

    def check_pass(self):
        user = self.database_manager.selectUserById(self.user_id)
        if self.do_hash(self.passw_entry.get()) == user.password: # porque guardo la contraseña hasheada
            Messagebox.show_info(title="Éxito",message="Contraseña correcta. Cambios confirmados")
            self.limpiar()
        else: 
            Messagebox.show_error(title="Error",message="Contraseña incorrecta. Inténtalo de nuevo", alert=True)
        self.popup.destroy()

    def show_text_entry_dialog(self):
        self.popup = tk.Toplevel(self.principal)
        self.popup.geometry("400x200")
        self.popup.resizable(False, False)
        ttk.Label(self.popup, text="Introduce la contraseña para confirmar los cambios: ").place(x=30,y=20)
        self.passw_entry = ttk.Entry(self.popup, show="*", width=30)
        self.passw_entry.place(x=80,y=65)
        self.passw_entry.focus_set()
        ttk.Button(self.popup, text="Confirmar", bootstyle = SUCCESS, command=self.check_pass).place(x=300,y=160)

    