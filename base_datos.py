#written by jorge orlando miranda ñahui
import sqlite3
import os
import sys
#clase para crear un objeto para el manejo de base de datos en sqlite3
class classdb(object):
    def __init__(self,name=None):
        if name !=None and isinstance(name,str):
            self.nombre=name
        else:
            print("--ERROR--")
            sys.exit()
    def conectar(self):
        #determinar si la base de datos existe o no
        self.conn=sqlite3.connect(self.nombre+".db")
        self.estado=True
        #crear objeto cursor
        self.cursor=self.conn.cursor()
        #crear campos
        contenido="""
        create table if not exists usuarios
        (id INTEGER ,nombres text NOT NULL,apellidos text NOT NULL,dni text PRIMARY KEY)"""
        #crear la tabla si en caso no existe
        self.cursor.execute(contenido)
        #realizar cambios
        self.conn.commit()
        self.size_usuarios=self.num_usuarios()

    def cerrar(self):
        self.estado=False
        print("CONEXIÓN CERRADA")
        #cerrar la conexión
        self.conn.close()
    def leer(self):
        #devolver todo el contenido
        if self.estado==True:
            texto="SELECT * FROM usuarios"
            datos=self.conn.execute(texto)
            #conseguir todos los elementos
            datos=datos.fetchall()
            self.conn.commit()
            return datos
        else:
            print("CONEXIÓN CERRADA")
            sys.exit()
    #método para determinar el número de usuarios
    def num_usuarios(self):
        if self.estado==True:
            users=self.cursor.execute("SELECT COUNT (*) FROM usuarios")
            users=users.fetchall()
            users=users[0][0]
            self.size_usuarios=users
        return users
    #método para agregar un nuevo usuario
    def insertar(self,*args):
        #preguntar si esta activo la conexión con la base de datos .db
        if self.estado==True:
            #determinar si es correcto el número de DNI
            #8 digitos numericos
            if len(args[2])==8 and args[2].isnumeric()==True:
                # determinar si el usuario ya existe o es nuevo
                datos = self.cursor.execute("SELECT * FROM usuarios")
                dnis = [dni[3] for dni in datos.fetchall()]
                # comparar si el dni de entrada es igual a uno de estos
                existe = args[2] in dnis
                if existe == False:
                    #verificación para registrar el nuevo usuario
                    print("USUARIO ")
                    print("NOMBRES",args[0])
                    print("APELLIDO", args[1])
                    print("DNI" , args[2])
                    input("click PARA VERIFICAR LOS DATOS:")
                    # comando sql para insertar los datos de un usuario
                    # ----------------(nombres,apellidos,dni,edad)
                    texto = """insert into usuarios values(?,?,?,?)"""
                    # insertar los elementos a cada campo de la tabla
                    self.cursor.execute(texto, (self.size_usuarios,*args))
                    # realizar los cambios
                    self.conn.commit()
                else:
                    print("EL USUARIO YA ESTA REGISTRADO")
                    #sys.exit()
            else:
                print("ERROR DEL DNI")
                sys.exit()

        else:
            print("CONEXIÓN CERRADA")
            sys.exit()
    #método para eliminar un usuario de la la base de datos
    def eliminar(self,usuario):
        if self.estado:
            #eliminar usuario
            self.cursor.execute("DELETE FROM usuarios WHERE dni={}".format(usuario))
            #se elimino correctamente
            self.conn.commit()
        else:
            print("CONEXIÓN CERRADA")
#crear objeto para el manejo de base de datos usuarios.db
b1=classdb("usuarios")
#conectarse a la base de datos
b1.conectar()
#agregar un usuario
#nombre, apellido , dni
datos=("tu_nombre","tu_apellido","74451458")
#usar el unpacking
b1.insertar(*datos)
#conseguir número de usuarios
datos2=b1.num_usuarios()
print("La cantidad de usuarios son : {}".format(datos2))
#mostrar todo el contenido
print("El contenido de la base de datos es:")
contenido=b1.leer()
for x in contenido:
    print(x)