from cryptography.fernet import Fernet

#módulo con métodos para encriptar y desencriptar
#tanto encrypt como decrypt trabajan con bytes

#ejemplo fianafHIASNlasfiAankdak-NkskOJKSLs=
#contraseña de ejemplo, pendiente añadir archivo configuración
key = Fernet.generate_key() 
def encrypted(password:str):
    #f = Fernet(b"fianafHIASNlasfiAankdak_NkskOJKSLs=") 
    #f = Fernet(key)
    f = Fernet(b"gAAAAABmNkBDdLrGq5LN8b_k8_fSTy6SBRmtaWKNkiDa8MXVe0J9MDcGTaneREop87bsX57MSOmZKqBn5h2fw33piF_ycIbOmWLyJVViSjqXqh4kNTYu4xM=")
    b_password = bytes(password, "ascii")
    encrypted_password = f.encrypt(b_password)
    return encrypted_password.decode("ascii")

def decrypt(password:str):
    #f = Fernet(b"fianafHIASNlasfiAankdak_NkskOJKSLs=")
    #f = Fernet(key)
    f = Fernet(b"gAAAAABmNkBDdLrGq5LN8b_k8_fSTy6SBRmtaWKNkiDa8MXVe0J9MDcGTaneREop87bsX57MSOmZKqBn5h2fw33piF_ycIbOmWLyJVViSjqXqh4kNTYu4xM=")
    b_password = bytes(password, "ascii")
    b_password_decrypt = f.decrypt(b_password)
    return b_password_decrypt.decode("ascii")