from ttkbootstrap import *


class AddOtro(Frame):
    def __init__(self, id, lista_estantes: list, master = None):
        super().__init__(master)
        self.user_id = id
        self.estantes = lista_estantes
        self.principal = master
        self.widgets()
    
    def widgets(self):
        lbl = Label(self.principal, text="PANTALLA OTROS",bootstyle=PRIMARY)
        lbl.place(x=300,y=300)

