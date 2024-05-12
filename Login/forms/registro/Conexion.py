import mysql.connector #pip install mysql-connector-python

class CConexion():
    def ConexionBaseDeDatos(usuario, passw, db_usuario):
        try:
            # Se establecen los parámetros de conexión
            conexion = mysql.connector.connect(user=usuario,password=passw,host='127.0.0.1',database=db_usuario,port='3306')
            #conn = mysql.connector.connect(**config)
            print("Conexión correcta")
            
            return conexion

        except mysql.connector.Error as error:
            print("Error: {}".format(error))

            return conexion
        
    #ConexionBaseDeDatos()