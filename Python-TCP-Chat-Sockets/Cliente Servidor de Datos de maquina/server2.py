# Inicia libreria que contendra los datos del Host y el puerto
import socket  

# Inicia Libreria encargada de abrir hilos de mensajes
import threading 

host = '127.0.0.1' # direccion IP del servidor
port = 55555 # puerto con el se comunicaran los hosts

# socket AF_INET = se usa socket tipo internet que usara el nombre de dominio o direccion IPv4 y un puerto,
# SOCK_STREAM = que usara protocolo tcp
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# se crea una variable con una funcion bind que contendra los datos de conexion
server.bind((host, port)) 

# que este a la escucha
server.listen() 

# indica en que IP y Puerto esta funcionando el servidor
print(f" El servidor funciona en {host}:{port}")

# lista, almacenara las conexiones o IP de los clientes
clients = [] 

# lista, almacenara los nombres de los nombres de los clientes
usernames = []

# envia mensajes a todos los clientes
def broadcast(message, _client):
    # utiliza las listas para obtener los datos del Cliente
    for client in clients: 
        # no envia el mensaja al emisor del mensaje, tiene que ser diferente para enviar
        if client != _client: 
            client.send(message)

# maneja los mensajes de cada usuario
def handle_messages(client):
    # loop infinito de escucha
    while True: 
        try:
            # lee solo 1024 bits, lo almacena en una variable
            message = client.recv(1024)
            # llama a la funcion boadcast
            broadcast(message, client) 

        # si existe error comienza esta funcion
        except: 
            # inicia variable con el listado de clientes en un index
            index = clients.index(client) 

            # localiza Usuario de la lista
            username = usernames[index]
            
            # llama a la funcion broadcast, envia a todos el usuario desconectado
            broadcast(f"ChatBot: {username} desconectado".encode('utf-8'), client)

            # remueve la direccion del cliente de la lista
            clients.remove(client)

            # remueve el nombre del cliente de la lista
            usernames.remove(username)

            # cierra la conexion
            client.close()
            
            #rompe el loop
            break

# funcion para aceptar y manejar las conexiones
def receive_connections(): 
    # loop infinito
    while True: 

        # acepta usuario IP y Puerto
        client, address = server.accept() 

        # Envia mensaje al cliente pidiendo el nombre, codificado en texto plano utf-8
        client.send("@username".encode("utf-8")) 
        username = client.recv(1024).decode('utf-8') 
        print(f" {username} se conecto con la direccion: {str(address)}")

        client.send("NomEquipo".encode("utf-8"))
        nombre_equipo = client.recv(1024).decode('utf-8')
        print("\n ========== Datos de Red ==========")
        print(f" El nombre del equipo es: {nombre_equipo}")
        
        client.send("ipEquipo".encode("utf-8"))
        direccion_equipo = client.recv(1024).decode('utf-8')
        print(f" La direccion de Red del equipo es: {direccion_equipo}")

        client.send("sistema".encode("utf-8"))
        sistema = client.recv(1024).decode('utf-8')
        print("\n ========== Sistema Operativo ==========")
        print(f" {sistema}")

        client.send("version".encode("utf-8"))
        version = client.recv(1024).decode('utf-8')
        print(f" {version}")

        client.send("procesador".encode("utf-8"))
        procesador = client.recv(1024).decode('utf-8')
        print("\n ========== Procesadores ==========")
        print(f" {procesador}")

        client.send("nucleos".encode("utf-8"))
        nucleos = client.recv(1024).decode('utf-8')
        print(f" {nucleos}")

        client.send("nucleosT".encode("utf-8"))
        nucleosT = client.recv(1024).decode('utf-8')
        print(f" {nucleosT}")

        client.send("maxFrec".encode("utf-8"))
        maxFrec = client.recv(1024).decode('utf-8')
        print(f" {maxFrec}")
        
        client.send("minFrec".encode("utf-8"))
        minFrec = client.recv(1024).decode('utf-8')
        print(f" {minFrec}")

        client.send("memoriaT".encode("utf-8"))
        memoriaT = client.recv(1024).decode('utf-8')
        print(f"\n ========== Memoria ==========")
        print(f" {memoriaT}")

        client.send("memoriaL".encode("utf-8"))
        memoriaL = client.recv(1024).decode('utf-8')
        print(f" {memoriaL}")

        client.send("memoriaU".encode("utf-8"))
        memoriaU = client.recv(1024).decode('utf-8')
        print(f" {memoriaU}")

        client.send("espacioDis".encode("utf-8"))
        espacioDis = client.recv(1024).decode('utf-8')
        print(f"\n ========== Disco Local C ==========")
        print(f" {espacioDis}")

        client.send("espacioDisL".encode("utf-8"))
        espacioDisL = client.recv(1024).decode('utf-8')
        print(f" {espacioDisL}")

        client.send("espacioDisU".encode("utf-8"))
        espacioDisU = client.recv(1024).decode('utf-8')
        print(f" {espacioDisU}")

        client.send("espacioDisD".encode("utf-8"))
        espacioDisD = client.recv(1024).decode('utf-8')
        print(f"\n ========== Disco Local D ==========")
        print(f" {espacioDisD}")

        client.send("espacioDisLD".encode("utf-8"))
        espacioDisLD = client.recv(1024).decode('utf-8')
        print(f" {espacioDisLD}")

        client.send("espacioDisUD".encode("utf-8"))
        espacioDisUD = client.recv(1024).decode('utf-8')
        print(f" {espacioDisUD}")

        client.send("procesos".encode("utf-8"))
        procesos = client.recv(1024).decode('utf-8')
        print(f"\n ========== Procesos Ejecutandose ==========")
        print(f"{procesos}")

        # se agrega la conexion cliente a la lista
        clients.append(client) 

        # se agrega el nombre a la lista de usuarios
        usernames.append(username) 
        
        # se muestra en la terminal del servidor el cliente conectado y su direccion
        

        # se muestra enla terminal de los clientes el nombre del cliente que se unio al chat
        message = f"ChatBot: {username} se ha unido al chat".encode("utf-8") 

        # se utiliza la funcion boadcast para enviar el mensaje a todos los conectados
        broadcast(message, client) 

        # se informa al cliente que se conecto al servidor
        client.send("Conectado al servidor".encode("utf-8")) 

        # Libreria threadin permite crear hilo por cada cliente con la funcion handle_messages
        thread = threading.Thread(target=handle_messages, args=(client,)) 

        # que comience la variable thread
        thread.start() 

# da inicio a la funicon receive_connections
receive_connections()