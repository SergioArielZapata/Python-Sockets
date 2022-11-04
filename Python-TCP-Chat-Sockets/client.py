# Inicia libreria que contendra los datos de la dupla Host y puerto
import socket 

# Inicia Libreria encargada de abrir hilos de mensajes
import threading 

# pide el nombre del usuario para ser agregado a la lista del servidor
username = input("Ingrese su Nombre: ")

host = '127.0.0.1' # direccion IP del Servidor
port = 55555 # puerto con el que se comunicaran los hosts al servidor

# socket AF_INET = se usa socket tipo internet que usara el nombre de dominio o direccion IPv4 y un puerto,
# SOCK_STREAM = que usara protocolo tcp
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Funcion connect, conecta con el servidor
client.connect((host, port)) 

# funcion que recibe los mensajes del servidor
def receive_messages():

    # comienza bucle infinito a la escucha del servidor
    while True: 
        try:
            # recibe mensaje del servidor solo de 1024 bits en texto plano utf-8
            message = client.recv(1024).decode('utf-8') 

            # si el mensaje del servidor es @usrename envia el nombre del usuario al servidor
            if message == "@username":

                # envia nombre usuario
                client.send(username.encode("utf-8"))
            else:

                # imprime mensaje del servidor
                print(message) 

        # si hay error ejecuta la excepcion
        except: 
            print("A ocurrido un error")
            
            # se cierra la conexion
            client.close

            # rompe el bucle si hay error
            break 

# fuincion para enviar mensaje al servidor
def write_messages(): 

    # comienza bucle infinito para la consola
    while True: 
            # pide mensaje al usuario
            mess = f"{input('')}"
            message = f"{username} : {mess}"

            # envia mensaje al servidor y el servidor a los demas con texto plano utf-8
            client.send(message.encode('utf-8'))
            
            # si el usuario escribe la palabra exit cierra la conexión y rompe el bucle
            if mess == "exit":
            
                # se cierra la conexion
                client.close
            
                # rompe el bucle
                break 


# crea hilo para recibir mensaje con la fucncion threading
receive_thread = threading.Thread(target=receive_messages) 

# inicia funcion receive_thread
receive_thread.start()

# crea hilo para enviar mensaje con la funcion threading
write_thread = threading.Thread(target=write_messages) 

# inicia funcion write_thread
write_thread.start()