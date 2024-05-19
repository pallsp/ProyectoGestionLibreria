"""import os
import tkinter as tk
from tkinter import Listbox, Scrollbar, Button, Label, messagebox

class CustomFileDialog(tk.Toplevel):
    def __init__(self, parent, initialdir='/', filetypes=[('PDF files', '*.pdf')], *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.initialdir = initialdir
        self.filetypes = filetypes
        self.selected_file = None
        
        self.title("Select a PDF file")
        self.geometry("600x400")

        self.current_path = initialdir
        self.create_widgets()
        self.list_directory(initialdir)
        
    def create_widgets(self):
        self.dir_label = Label(self, text=self.current_path)
        self.dir_label.pack(pady=5)
        
        self.listbox = Listbox(self, selectmode=tk.SINGLE, width=80, height=20)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = Scrollbar(self, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.select_button = Button(self, text="Select", command=self.select_file)
        self.select_button.pack(side=tk.BOTTOM, pady=5)
        
        self.listbox.bind('<Double-1>', self.on_double_click)

    def list_directory(self, path):
        self.listbox.delete(0, tk.END)
        self.dir_label.config(text=path)
        self.current_path = path
        
        try:
            items = os.listdir(path)
            items = sorted(item for item in items if not item.startswith('.'))
            for item in items:
                self.listbox.insert(tk.END, item)
        except PermissionError:
            messagebox.showerror("Error", "You do not have permission to access this folder.")
        
    def on_double_click(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            value = self.listbox.get(index)
            full_path = os.path.join(self.current_path, value)
            
            if os.path.isdir(full_path):
                self.list_directory(full_path)
            elif full_path.lower().endswith('.pdf'):
                self.selected_file = full_path
                self.destroy()
    
    def select_file(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            value = self.listbox.get(index)
            full_path = os.path.join(self.current_path, value)
            
            if os.path.isdir(full_path):
                self.list_directory(full_path)
            elif full_path.lower().endswith('.pdf'):
                self.selected_file = full_path
                self.destroy()
    
    def show(self):
        self.wait_window()
        return self.selected_file

def open_custom_dialog():
    dialog = CustomFileDialog(root, initialdir=os.path.expanduser('~'), filetypes=[('PDF files', '*.pdf')])
    selected_file = dialog.show()
    if selected_file:
        print(f"Selected file: {selected_file}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("200x100")
    open_button = Button(root, text="Open Custom File Dialog", command=open_custom_dialog)
    open_button.pack(pady=20)
    root.mainloop()
"""

import os
import tkinter as tk
from tkinter import Button, Label, messagebox, Toplevel
from tkinter import ttk

class CustomFileDialog(Toplevel):
    def __init__(self, parent, initialdir='/', filetypes=[('PDF files', '*.pdf')], *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.initialdir = initialdir
        self.filetypes = filetypes
        self.selected_file = None
        
        self.title("Select a PDF file")
        self.geometry("800x600")
        self.config(bg="#2e2e2e")

        self.current_path = initialdir
        self.create_widgets()
        self.list_directory(initialdir)
        
    def create_widgets(self):
        self.dir_label = Label(self, text=self.current_path, bg="#2e2e2e", fg="#ffffff")
        self.dir_label.pack(pady=5)
        
        self.canvas = tk.Canvas(self, bg="#2e2e2e")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.frame = tk.Frame(self.canvas, bg="#2e2e2e")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.select_button = Button(self, text="Select", command=self.select_file, bg="#4CAF50", fg="#ffffff")
        self.select_button.pack(side=tk.BOTTOM, pady=5)
        
    def list_directory(self, path):
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        self.dir_label.config(text=path)
        self.current_path = path
        
        try:
            items = os.listdir(path)
            items = sorted(item for item in items if not item.startswith('.'))
            row, col = 0, 0
            for item in items:
                full_path = os.path.join(self.current_path, item)
                if os.path.isdir(full_path):
                    item_label = Label(self.frame, text=item, bg="#3e3e3e", fg="#ffffff", width=20, height=2, relief="groove")
                elif item.lower().endswith('.pdf'):
                    item_label = Label(self.frame, text=item, bg="#616161", fg="#ffffff", width=20, height=2, relief="groove")
                else:
                    continue
                
                item_label.grid(row=row, column=col, padx=5, pady=5)
                item_label.bind("<Double-1>", lambda e, path=full_path: self.on_double_click(path))
                col += 1
                if col >= 6:
                    col = 0
                    row += 1
        except PermissionError:
            messagebox.showerror("Error", "You do not have permission to access this folder.")
        
    def on_double_click(self, full_path):
        if os.path.isdir(full_path):
            self.list_directory(full_path)
        elif full_path.lower().endswith('.pdf'):
            self.selected_file = full_path
            self.destroy()
    
    def select_file(self):
        selected_item = self.frame.focus_get()
        if selected_item:
            full_path = selected_item.cget("text")
            full_path = os.path.join(self.current_path, full_path)
            if os.path.isdir(full_path):
                self.list_directory(full_path)
            elif full_path.lower().endswith('.pdf'):
                self.selected_file = full_path
                self.destroy()
    
    def show(self):
        self.wait_window()
        return self.selected_file

def open_custom_dialog():
    dialog = CustomFileDialog(root, initialdir=os.path.expanduser('~'), filetypes=[('PDF files', '*.pdf')])
    selected_file = dialog.show()
    if selected_file:
        print(f"Selected file: {selected_file}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("200x100")
    open_button = Button(root, text="Open Custom File Dialog", command=open_custom_dialog)
    open_button.pack(pady=20)
    root.mainloop()
