from cryptography.fernet import Fernet

#módulo con métodos para encriptar y desencriptar
#tanto encrypt como decrypt trabajan con bytes

def encrypted(password:str):
    f = Fernet(b"fianafHIASNlasfiAankdak-NkskOJKSLs=") #contraseña de ejemplo, pendiente añadir archivo configuración 
    b_password = bytes(password, "ascii")
    encrypted_password = f.encrypt(b_password)
    return encrypted_password.decode("ascii")

def decrypt(password:str):
    f = Fernet(b"fianafHIASNlasfiAankdak-NkskOJKSLs=")
    b_password = bytes(password, "ascii")
    b_password_decrypt = f.decrypt(b_password)
    return b_password_decrypt.decode("ascii")