import socket
import threading

# Función para solicitar y validar el nombre de usuario
def obtener_nombre_usuario():
    while True:
        nombre_usuario = input("Ingresa tu nombre de usuario: ")
        if nombre_usuario.strip():  # Verificar si el nombre de usuario no está vacío
            return nombre_usuario
        else:
            print("El nombre de usuario no puede estar vacío. Por favor, ingresa un nombre de usuario válido.")

# Obtener el nombre de usuario
nombre_usuario = obtener_nombre_usuario()

# Mensaje de conexión exitosa al servidor
print("Conexión exitosa al servidor.")


# Función para manejar la recepción de mensajes
def recibir_mensajes(cliente_socket):
    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode('utf-8')
            print(mensaje)
        except:
            # Si ocurre un error, salir del bucle
            break

# Configurar el socket del cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor_ip = input("Ingresa la dirección IP del servidor: ")
servidor_puerto = int(input("Ingresa el puerto del servidor: "))
cliente.connect((servidor_ip, servidor_puerto))

# Iniciar un hilo para recibir mensajes
thread_recv = threading.Thread(target=recibir_mensajes, args=(cliente,))
thread_recv.start()

# Enviar mensajes al servidor
while True:
    print('**ESCRIBE UN MENSAJE**')
    mensaje = input()
    if mensaje.strip():  # Verificar si el mensaje no está vacío después de eliminar espacios en blanco
        if mensaje == "/listar":
            cliente.send(mensaje.encode('utf-8'))
        elif mensaje == "/quitar":
            cliente.send(mensaje.encode('utf-8'))
            break
        else:
            cliente.send(f'{nombre_usuario}: {mensaje}'.encode('utf-8'))
    else:
        print("No puedes enviar un mensaje vacío. Escribe algo.")

# Cerrar el socket del cliente
cliente.close()
