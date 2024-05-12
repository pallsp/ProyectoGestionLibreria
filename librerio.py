import subprocess

MARCADOR_BASE_DATOS = "base_datos_creada.txt"

def build_launch_base_datos():
    subprocess.run(["python3", "Login/build_db.py"])
    with open(MARCADOR_BASE_DATOS, "w") as archivo:
        archivo.write("1\n")

def ejecutar_login():
    # Ejecutar login.py como un proceso separado
    resultado_login = subprocess.run(["python3", "Login/main.py"], capture_output=True)
    resultado = resultado_login.stdout.strip().decode()
    return resultado
def ejecutar_app(user_id):
    # Ejecutar app.py como un proceso separado
    subprocess.run(["python3", "App/guimoderna/app.py", str(user_id)]) # le paso como argumento el id de usuario

def main():
    try:
        with open(MARCADOR_BASE_DATOS, "r") as archivo:
            print("Base de datos ya creada")
    except FileNotFoundError:
        print("Base de datos no creada todavía")
        build_launch_base_datos() # ejecutar el script de creación de la base de datos
    
    user_id = ejecutar_login() # obtengo el id del usuario que acaba de iniciar sesión
    print("Id de usuario: ", user_id)
    ejecutar_app(user_id)

if __name__ == "__main__":
    main()