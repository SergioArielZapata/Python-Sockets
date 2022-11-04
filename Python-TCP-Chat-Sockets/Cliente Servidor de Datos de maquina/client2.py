import socket 
import threading 
import psutil
import platform
import os
my_system = platform.uname()
cpufreq = psutil.cpu_freq()
svmem = psutil.virtual_memory()
disk_usage = psutil.disk_usage("C:\\")
disk_usage2 = psutil.disk_usage("D:\\")
output = os.popen('wmic process get description, processid').read()

# pide el nombre del usuario para ser agregado a la lista del servidor
username = input("Ingrese su Nombre: ")

host = '127.0.0.1' # direccion IP del Servidor
port = 55555 # puerto con el que se comunicaran los hosts al servidor

# socket AF_INET = se usa socket tipo internet que usara el nombre de dominio o direccion IPv4 y un puerto,
# SOCK_STREAM = que usara protocolo tcp
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Funcion connect, conecta con el servidor
client.connect((host, port)) 

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit} {suffix}"
        bytes /= factor

# funcion que recibe los mensajes del servidor
def receive_messages():

    # comienza bucle infinito a la escucha del servidor
    while True: 
        try:
            # recibe mensaje del servidor solo de 1024 bits en texto plano utf-8
            message = client.recv(1024).decode('utf-8') 

            # si el mensaje del servidor es @usrename envia el nombre del usuario al servidor
            if message == "@username":
                client.send(username.encode("utf-8"))

            if message == "NomEquipo": 
                nombre_equipo = socket.gethostname()
                client.send(nombre_equipo.encode("utf-8"))
            
            if message == "ipEquipo":
                direccion_equipo = socket.gethostbyname(nombre_equipo)
                client.send(direccion_equipo.encode("utf-8"))

            if message == "sistema":
                sistema = (f"Sistema: {my_system.system}")
                client.send(sistema.encode("utf-8"))

            if message == "version":
                version = (f"Version: {my_system.version}")
                client.send(version.encode("utf-8"))
                
            if message == "procesador":
                procesador = (f"Procesador: {my_system.processor}")
                client.send(procesador.encode("utf-8"))

            if message == "nucleos":
               nucleos = (f"Nucleos Fisicos: {psutil.cpu_count(logical=False)} ")
               client.send(nucleos.encode("utf-8"))

            if message == "nucleosT":
               nucleosT = (f"Total de Nucleos: {psutil.cpu_count(logical=True)} ")
               client.send(nucleosT.encode("utf-8"))

            if message == "maxFrec":
               maxFrec = (f"Frecuencia Maxima: {cpufreq.max: .2f} Mhz ")
               client.send(maxFrec.encode("utf-8"))

            if message == "minFrec":
               minFrec = (f"Frecuencia Minima: {cpufreq.min: .2f} Mhz ")
               client.send(minFrec.encode("utf-8"))

            if message == "memoriaT":
               memoriaT = (f"Memoria Total: {get_size (svmem.total)}")
               client.send(memoriaT.encode("utf-8"))
            
            if message == "memoriaL":
               memoriaL = (f"Memoria Libre: {get_size (svmem.available)}")
               client.send(memoriaL.encode("utf-8"))
            
            if message == "memoriaU":
               memoriaU = (f"Memoria Usada: {get_size (svmem.used)}")
               client.send(memoriaU.encode("utf-8"))

            if message == "espacioDis":
               espacioDis = (f"Espacio total Disco C: {get_size(disk_usage.total)}")
               client.send(espacioDis.encode("utf-8"))
            
            if message == "espacioDisL":
               espacioDisL = (f"Espacio Libre Disco C: {get_size(disk_usage.free)}")
               client.send(espacioDisL.encode("utf-8"))
            
            if message == "espacioDisU":
               espacioDisU = (f"Espacio Usado Disco C: {get_size(disk_usage.used)}")
               client.send(espacioDisU.encode("utf-8"))

            if message == "espacioDisD":
               espacioDisD = (f"Espacio total Disco D: {get_size(disk_usage2.total)}")
               client.send(espacioDisD.encode("utf-8"))
            
            if message == "espacioDisLD":
               espacioDisLD = (f"Espacio Libre Disco D: {get_size(disk_usage2.free)}")
               client.send(espacioDisLD.encode("utf-8"))
            
            if message == "espacioDisUD":
               espacioDisUD = (f"Espacio Usado Disco D: {get_size(disk_usage2.used)}")
               client.send(espacioDisUD.encode("utf-8"))

            if message == "procesos":
               procesos = (f"{output}")
               client.send(procesos.encode("utf-8"))             

            if message != "@username" and message !="NomEquipo" and message != "ipEquipo" and message != "sistema" and message != "version" and message != "procesador" and message != "memoriaU" and message != "memoriaL" and message != "memoriaT" and message != "nucleos" and message != "nucleosT" and message != "maxFrec" and message != "minFrec" and message != "espacioDis" and message != "espacioDisL" and message != "espacioDisU" and message != "espacioDisD" and message != "espacioDisLD" and message != "espacioDisUD" and message != "procesos":
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