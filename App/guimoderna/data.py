import sqlite3

class Datos:
    @classmethod
    def crear(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS libros(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       titulo VARCHAR(100), 
                       autor VARCHAR(40),
                       idioma VARCHAR(30),
                       editorial varchar(80)
                       )
                       """)
        conn.commit()
        conn.close()
        print("base de datos creada con exito")
    @classmethod
    def guardar(self, sql,parametros=()):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(sql,parametros)
        conn.commit()
        conn.close()
    @classmethod
    def recuperar(self,sql,parametros=()):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(sql,parametros)
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        return datos