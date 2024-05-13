from ttkbootstrap import * 
from add_libros import AddLibro
from add_otros import AddOtro
from ttkbootstrap.dialogs import Messagebox
import hashlib
from persistence.repository.database_manager import DatabaseManager

class AddDocumentos(Frame):
    def __init__(self, id, lista_estantes: list, master = None):
        super().__init__(master)
        self.database_manager = DatabaseManager()
        self.user_id = id
        self.estantes = lista_estantes
        self.principal = master
        self.widgets()
    
    def widgets(self):
        # BOTONES CENTRALES
        #font_botones = font.Font(family= "Times", size= 20, weight= "bold")
        btnlibros = Button(self.principal,text="LIBRO", bootstyle = SUCCESS, command=lambda: self.show_confirm_passw("libros"))
        #btnlibros.config(font=("Times", 20))
        btnlibros.place(x=300, y=300, width=200, height=150)

        btnotro = Button(self.principal, text="OTRO", bootstyle = DANGER, command=lambda: self.show_confirm_passw("otro"))
        #btnotro.config(font=("Times", 20))
        btnotro.place(x=520, y=300, width=200, height=150)

    def limpiar_pantalla(self, panel):
        for widget in panel.winfo_children():
            widget.destroy()

    def add_libro(self):
        self.limpiar_pantalla(self.principal)
        pantalla_documentos = AddLibro(self.user_id, self.estantes, self.principal)
        pantalla_documentos.place(x=0, y=0, width=1260, height=710)

    def add_otro(self):
        self.limpiar_pantalla(self.principal)
        pantalla_documentos = AddOtro(self.user_id, self.estantes , self.principal)
        pantalla_documentos.place(x=0, y=0, width=1260, height=710)

    def check_pass(self, tipo):
        estado = False
        user = self.database_manager.selectUserById(self.user_id)
        if self.do_hash(self.passw_entry.get()) == user.password: # porque guardo la contraseña hasheada
            Messagebox.show_info(title="Éxito", message=f"Contraseña correcta. Puedes añadir {tipo}.")
            estado = True
        else: 
            Messagebox.show_error(title="Error", message="Contraseña incorrecta. Inténtalo de nuevo", alert=True)
        self.popup.destroy()
        if estado and tipo == "libros":
            self.add_libro()
        elif estado and tipo == "otro":
            self.add_otro()

    def show_confirm_passw(self, tipo):
        self.popup = tk.Toplevel(self.principal)
        self.popup.geometry("400x200")
        self.popup.resizable(False, False)
        ttk.Label(self.popup, text=f"Introduce la contraseña para poder añadir {tipo}: ").place(x=30,y=20)
        self.passw_entry = ttk.Entry(self.popup, show="*", width=30)
        self.passw_entry.place(x=80,y=65)
        self.passw_entry.focus_set()
        ttk.Button(self.popup, text="Confirmar", bootstyle = SUCCESS, command=lambda: self.check_pass(tipo)).place(x=300,y=160)

    # HASH
    def do_hash(self, texto: str):
        hasher = hashlib.sha3_512()
        hasher.update(texto.encode('utf-8'))
        return hasher.hexdigest() 
        

    