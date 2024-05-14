from sqlalchemy import Column, String, Integer, Table, ForeignKey, Date, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
#nuestras tablas en la base de datos
Base = declarative_base()

#tablas intermedias para las relaciones muchos a muchos
"""documento_estante = Table('documento_estante', Base.metadata, 
                          Column("documento_id", Integer, ForeignKey("documento.id"), primary_key=True), 
                          Column("estante_id", Integer, ForeignKey("estante.id"), primary_key=True)
                        )"""

class Auth_User(Base):
    __tablename__ = "auth_user"
    id = Column(Integer, primary_key = True, autoincrement = True)
    username = Column(String(150))
    password = Column(String(128))

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    password = Column(String(500), nullable=False)
    correo = Column(String(100), nullable=False)
    foto = Column(String(250))

    #relación con la tabla cuenta 
    cuenta = relationship("Cuenta", uselist=False, back_populates="usuario")

    #relación con la tabla biblioteca
    biblioteca = relationship("Biblioteca", uselist=False, back_populates="propietario")

class Cuenta(Base):
    __tablename__ = "cuenta"
    usuario_id = Column(Integer, ForeignKey("usuario.id"), primary_key=True)
    fecha_creacion = Column(Date)

    #relación con la tabla usuario
    usuario = relationship("Usuario", back_populates="cuenta")

class Biblioteca(Base):
    __tablename__ = "biblioteca"
    id = Column(String(50), primary_key=True)
    propietario_id = Column(Integer, ForeignKey("usuario.id"), primary_key=True)
    fecha_creacion = Column(Date)

    #relación con la tabla usuario
    propietario = relationship("Usuario", back_populates="biblioteca")

    #relación con la tabla estantes
    estantes = relationship("Estante", back_populates="biblioteca")

class Estante(Base):
    __tablename__ = "estante"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    propietario_id = Column(Integer, ForeignKey("biblioteca.propietario_id"), primary_key=True)
    tematica = Column(String(50))
    tamano = Column(Integer, nullable=False)
    fecha_creacion = Column(Date)
    fecha_modificacion = Column(Date)
    tipo = Column(Enum("LIBROS", "OTROS", "LIBROS/OTROS"))

    #relación con la tabla biblioteca
    biblioteca = relationship("Biblioteca", back_populates="estantes")

    #relación con la tabla documento
    documentos = relationship("Documento", secondary="documento_estante", back_populates="estantes")

class DocumentoEstante(Base):
    __tablename__ = "documento_estante"

    documento_id = Column(Integer, ForeignKey('documento.id'), primary_key=True)
    estante_id = Column(Integer, ForeignKey('estante.id'), primary_key=True)

class Formato(Base):
    __tablename__ = "formato"
    id = Column(Integer, primary_key=True) # 1000 -> FÍSICO 1001 -> PDF EN UN FUTURO EPUB
    tipo = Column(String(35), nullable=False, unique=True)

    #relación con la tabla documento
    documentos = relationship("Documento", back_populates="formato")

class Documento(Base):
    __tablename__ = "documento"
    id = Column(Integer, primary_key=True, autoincrement=True)
    estante = Column(Integer, ForeignKey("estante.id"), nullable=True)
    propietario_id = Column(Integer, ForeignKey("usuario.id"), primary_key=True)
    titulo = Column(String(100), nullable=False)
    autor = Column(String(100), nullable=False)
    formato_id = Column(Integer, ForeignKey("formato.id"), nullable=False)      #Column(Enum("FÍSICO", "PDF"))  # en un futuro EPUB  
    idioma = Column(String(20))
    tipo = Column(Enum("Libro", "Otro"), nullable=False) #tipo de documento
    
    #relación con la tabla formato
    formato = relationship("Formato", back_populates="documentos")

    #relación con la tabla estante
    estantes = relationship("Estante", secondary="documento_estante", back_populates="documentos")

    #relación con la tabla libro
    libro = relationship("Libro", uselist=False, back_populates="documento")

    #relación con la tabla otro 
    otro = relationship("Otro", uselist=False, back_populates="documento")

class Genero(Base):
    __tablename__ = "genero"
    nombre = Column(String(50), primary_key=True)

    #relación con la tabla libro
    libros = relationship("Libro", back_populates="genero")

    #relación con la tabla categoría
    categorias = relationship("Categoria", back_populates="genero")

class Categoria(Base):
    __tablename__ = "categoria"
    nombre = Column(String(50), primary_key=True)
    nombre_genero = Column(String(50), ForeignKey("genero.nombre"))

    #relación con la tabla libro 
    libros = relationship("Libro", back_populates="categoria")

    #relación con la tabla género
    genero = relationship("Genero", back_populates="categorias")

class Libro(Base):
    __tablename__ = "libro"
    isbn = Column(String(100), primary_key=True) # se podría utilizar BigInteger
    id_documento = Column(Integer, ForeignKey("documento.id"), primary_key=True, unique=True)
    propietario_id = Column(Integer, ForeignKey("usuario.id"), primary_key=True)
    fecha_publicacion = Column(Date)
    editorial = Column(String(50), nullable=False)
    tematica = Column(String(50))
    nombre_genero = Column(String(50), ForeignKey("genero.nombre"))
    nombre_categoria = Column(String(50), ForeignKey("categoria.nombre"))

    #relación con la tabla documento
    documento = relationship("Documento", uselist=False, back_populates="libro")
    
    #relación con la tabla género
    genero = relationship("Genero", back_populates="libros")

    #relación con la tabla categoría
    categoria = relationship("Categoria", back_populates="libros")

class Otro(Base):
    __tablename__ = "otro"
    id = Column(Integer, ForeignKey("documento.id"), primary_key=True)
    propietario_id = Column(Integer, ForeignKey("usuario.id"), primary_key=True)
    emisor = Column(String(50))
    fecha = Column(Date)
    tipo = Column(String(50), nullable=False)
    subtipo = Column(String(50), nullable=False)

    #relación con la tabla documento 
    documento = relationship("Documento", uselist=False, back_populates="otro")
