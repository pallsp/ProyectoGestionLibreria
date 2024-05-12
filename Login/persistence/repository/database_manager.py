import sqlalchemy as db 
from persistence.model import *
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
import hashlib

#gestionamos la conectividad a nuestra base de datos
class DatabaseManager():
    def __init__(self):
        #self.engine = db.create_engine(f'mysql://{usuario}:{passw}@localhost/{db_usuario}')
        self.engine = db.create_engine('mysql://root:Bluegamerin1220@localhost/db_librerio')
        self.Session = sessionmaker(bind=self.engine)
        #Session = sessionmaker(self.engine)
        #self.session = Session()
        # engine = create_engine('mysql://usuario:contraseña@localhost:puerto/nombre_de_la_base_de_datos'), el puerto se indica si es distinto del predeterminado
    
    #with sessionmaker(self.engine) as session:
    #with Session(self.engine) as session:


    # ----------TABLA USUARIO---------- 

    # INSERT USUARIO
    def insertUser(self, usuario: Usuario):
        try:
            session = self.Session()
            session.add(usuario)
            session.commit()

            session.execute(text(f"CREATE USER IF NOT EXISTS '{usuario.nombre}'@'localhost' IDENTIFIED BY '{usuario.password}'"))
            session.execute(text(f"GRANT ALL PRIVILEGES ON db_librerio.* TO '{usuario.nombre}'@'localhost'"))
            session.commit()
            #print("Usuario creado con éxito en el gestor de mysql.")
            #try:
            #connection = mysql.connector.connect(
            #user = 'root',
            #password = 'Bluegamerin1220',
            #host = '127.0.0.1',
            #database = 'db_librerio',
            #port = '3306'
            #)
            #cursor = connection.cursor() # para poder crear consultas sql

            #cursor.execute(f"CREATE USER IF NOT EXISTS '{usuario.nombre}'@'localhost' IDENTIFIED BY '{usuario.password}'")
            #cursor.execute(f"GRANT ALL PRIVILEGES ON db_librerio.* TO '{usuario.nombre}'@'localhost'")
            #connection.commit()
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al crear el usuario en la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()

    # obtener usuario por nombre
    def getUserByUserName(self, user_name: str):
        user: Usuario = None
        try:
            session = self.Session()
            user = session.query(Usuario).filter_by(nombre = user_name).first()
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al obtener el usuario en la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()
        return user
    #with Session(self.engine) as session: 
    #user = session.query(Auth_User).filter_by(username = user_name).first()

    # UPDATE USUARIO
    def updateUsuario(self, id_usuario, new_user, new_passw, new_email, new_path: str):
        new_hash_passw = self.do_hash(new_passw)
        try:
            session = self.Session()
            session.query(Usuario).filter(Usuario.id == id_usuario).update(
                {Usuario.nombre:new_user, Usuario.password:new_hash_passw, Usuario.correo:new_email, Usuario.foto: new_path})
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al actualizar los datos del usuario en la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()

    # SELECT USUARIO POR ID
    def selectUserById(self, user_id):
        user: Usuario = None
        try:
            session = self.Session()
            user = session.query(Usuario).filter(Usuario.id == user_id).first()
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al obtener el usuario de la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()
        return user
    
    
    # ----------TABLA DOCUMENTO----------

    # INSERT DOCUMENTO
    def insertDocumento(self, doc: Documento):
        try:
            session = self.Session()
            session.add(doc)
            session.commit()
            print("Documento añadido con éxito a la base de datos.")
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al añadir el documento a la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()

        # ESTO SE PUEDE PROBAR PARA VER SI FUNCIONA
        #with Session(self.engine) as session:
            #session.add(doc)
            #session.commit()

    # DELETE DOCUMENTO
    def deleteDocumentoById(self, id):
        try:
            session = self.Session()
            doc = session.query(Documento).filter(Documento.id == id).one()
            session.delete(doc)
            session.commit()
            print("Documento eliminado con éxito a la base de datos.")
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al eliminar el documento a la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()

    # SELECT * FROM Documents WHERE id_propietario = id
    def selectDocumentsByIdOwner(self, id):
        try:
            session = self.Session()
            documentos = session.query(Documento).filter(Documento.propietario_id == id).all()
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al obtener los documentos de la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()
        return documentos

    # SELECT * FROM Documents WHERE id = id
    def selectDocumentsById(self, id):
        try:
            session = self.Session()
            documentos = session.query(Documento).filter(Documento.id == id).all()
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al obtener los documentos de la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()
        return documentos

    # SELECT * FROM Documents
    def selectAllDocumentos(self):
        try:
            session = self.Session()
            documentos = session.query(Documento).all()
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al obtener los documentos de la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()
        return documentos
    
    # SELECT * FROM Documents WHERE tipo = Libro
    def selectAllDocumentosLibros(self):
        try:
            session = self.Session()
            documentos = session.query(Documento).filter(Documento.tipo == "Libro").all()
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al obtener los documentos de la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()
        return documentos

    # UPDATE DOCUMENTO
    def updateDocumento(self, id_documento, titulo, autor, idioma, formato, estante):
        try:
            session = self.Session()
            session.query(Documento).filter(Documento.id == id_documento).update(
                {Documento.titulo:titulo, 
                 Documento.autor:autor, 
                 Documento.idioma:idioma, 
                 Documento.formato:formato, 
                 Documento.estante:estante})
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al actualizar los datos del documento en la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()
    
    # SELECT ID FROM DOCUMENT DEL ULTIMO DOCUMENTO AÑADIDO 
    def selectIdLastDocumento(self):
        documento = Documento()
        try:
            session = self.Session()
            documento = session.query(Documento).order_by(Documento.id.desc()).first()
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al obtener el documento de la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()
        return documento.id
    

        #PROBAR MAS TARDE
        #with Session(self.engine) as session: 
            #documents = session.query(Documento).all() 
            #for document in documents:
                #pass

    # ----------TABLA LIBRO---------- 

    # INSERT LIBRO
    def insertLibro(self, libro: Libro):
        try:
            session = self.Session()
            session.add(libro)
            session.commit()
            print("Libro añadido con éxito a la base de datos.")
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al añadir el libro a la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()

    # DELETE LIBRO
    def deleteLibro(self, libro: Libro):
        try:
            session = self.Session()
            session.delete(libro)
            session.commit()
            print("Libro eliminado con éxito a la base de datos.")
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al eliminar el libro a la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()

    # DELETE LIBRO POR ID
    def deleteLibroById(self, id):
        try:
            session = self.Session()
            libro = session.query(Libro).filter(Libro.id_documento == id).one()
            session.delete(libro)
            session.commit()
            print("Libro eliminado con éxito a la base de datos.")
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al eliminar el libro a la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()

    # SELECT * FROM libros WHERE id = id
    def selectLibrosById(self, id):
        try:
            session = self.Session()
            libros = session.query(Libro).filter(Libro.id_documento == id).all()
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al obtener los libros de la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()
        return libros

    # SELECT * FROM libros
    def selectAllLibros(self):
        libros = []
        try:
            session = self.Session()
            libros = session.query(Libro).all()
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al obtener los libros de la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()
        return libros

    # UPDATE LIBRO
    def updateLibro(self, id_documento, isbn, fecha_publicacion, editorial, tematica, genero, categoria):
        try:
            session = self.Session()
            session.query(Libro).filter(Libro.id_documento == id_documento).update(
                {Libro.isbn:isbn, 
                 Libro.fecha_publicacion:fecha_publicacion, 
                 Libro.editorial:editorial, 
                 Libro.tematica:tematica, 
                 Libro.nombre_genero:genero,
                 Libro.nombre_categoria:categoria})
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al actualizar los datos del libro en la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()


    # obtener todos los usuarios        
    def getUsers(self):
        with Session(self.engine) as session: 
            users = session.query(Usuario).all()
            return users

    # ----------TABLA ESTANTE----------

    # INSERT ESTANTE
    def insertEstante(self, est: Estante):
        with Session(self.engine) as session:
            pass
    
    # ----------TABLA FORMATO----------

    # INSERT FORMATO
    def insertFormato(self, formato):
        try:
            session = self.Session()
            session.add(formato)
            session.commit()
            print("Formato añadido con éxito a la base de datos.")
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al añadir el formato a la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()

    # SELECT * FROM FORMATO
    def selectFormatos(self):
        formatos = []
        try:
            session = self.Session()
            formatos = session.query(Formato).all()
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al obtener los formatos de la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()
        return formatos

    # SELECT * FROM FORMATO WHERE tipo = tipo
    def selectFormatoByTipo(self, tipo):
        formato = Formato()
        try:
            session = self.Session()
            formato = session.query(Formato).filter(Formato.tipo == tipo).first()
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al obtener el formato de la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()
        return formato

    # ----------TABLA GENERO----------

    # INSERT GÉNERO
    def insertGenero(self, genero):
        try:
            session = self.Session()
            session.add(genero)
            session.commit()
            print("Género añadido con éxito a la base de datos.")
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al añadir el género a la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()

    # SELECT NOMBRE FROM GÉNERO
    def selectGeneros(self):
        generos = []
        generos_f = []
        try:
            session = self.Session()
            generos = session.query(Genero.nombre).all()
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al obtener los géneros de la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()
        for genero in generos: 
            genero_f = genero[0]
            generos_f.append(genero_f)
        return generos_f

    # ----------TABLA CATEGORIA----------

    # INSERT CATEGORÍA
    def insertCategoria(self, categoria):
        try:
            session = self.Session()
            session.add(categoria)
            session.commit()
            print("Categoría añadida con éxito a la base de datos.")
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al añadir la categoría a la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()

    # SELECT NOMBRE FROM CATEGORÍA
    def selectCategorias(self):
        categorias = []
        categorias_f = []
        try:
            session = self.Session()
            categorias = session.query(Categoria.nombre).all()
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al obtener las categorías de la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()
        for categoria in categorias: 
            categoria_f = categoria[0]
            categorias_f.append(categoria_f)
        return categorias_f

    # ----------VARIOS----------
    
    # obtengo el id de un usuario por el nombre
    def selectUserId(self, name: str):
        try:
            session = self.Session()
            user = session.query(Usuario).filter(Usuario.nombre == name)
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al obtener el usuario de la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()
        return user

    # UPDATE FOTO 
    def updateFoto(self, id_usuario, new_path: str):
        try:
            session = self.Session()
            session.query(Usuario).filter(Usuario.id == id_usuario).update({Usuario.foto: new_path})
        except SQLAlchemyError as error:
            session.rollback()
            print(f"Error al actualizar la foto del usuario en la base de datos: {error}")
        finally:
            if session.is_active:
                session.close()

    # SELECT * FROM Documents WHERE titulo = tittle
    def selectDocumentsByTittle(self, tittle):
        with Session(self.engine) as session: 
            documents = session.query(Documento).filter(
                Documento.titulo == tittle
            ) #si quisieramos añadir otra condicion podriamos poner a continuacion otro .filter(lo que sea)
            for document in documents:
                pass
    
    # SELECT id FROM ESTANTES WHERE tematica = tem
    def selectEstanteByTematica(self, tem):
        with Session(self.engine) as session:
            estantes = session.query(Estante.id).filter(
                Estante.tematica == tem
            )
            for estante in estantes:
                pass
    #importante tener en cuenta que cuando ponemos clases nos devolvera instancias de dicha clase (objetos)
    #si ponemos argumentos, como en este último caso, nos devolvera tuplas

    def do_hash(self, texto: str):
        hasher = hashlib.sha3_512()
        hasher.update(texto.encode('utf-8'))
        return hasher.hexdigest() 