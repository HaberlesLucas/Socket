import socket
import threading

# ip y puerto del servidor
host = '127.0.0.1'
port = 1812

# para almacenar los clientes conectados
clientes = []

# función para enviar un mensaje a todos los clientes
def transmision(mensaje, cliente_enviador=None):
    for cliente in clientes:
        if cliente != cliente_enviador:
            try:
                cliente.send(mensaje)
            except:
                # Si hay un error al enviar el mensaje, desconectar al cliente.
                cliente.close()
                clientes.remove(cliente)

# función para manejar la comunicación con un cliente
def manejar_cliente(cliente, direccion):
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            if mensaje:
                if mensaje == "/listar":
                    # enviar la lista de usuarios conectados al cliente que la solicita
                    lista_usuarios = ", ".join([str(c.getpeername()) for c in clientes])
                    cliente.send(f'Usuarios conectados: {lista_usuarios}'.encode('utf-8'))
                elif mensaje == "/quitar":
                    # desconectar al cliente que envía el comando "/quitar"
                    cliente.close()
                    clientes.remove(cliente)
                    transmision(f'Cliente {direccion} se ha desconectado.\n'.encode('utf-8'))
                    break
                else:
                    # reenviar el mensaje a todos los clientes
                    mensaje_a_transmitir = f'Nuevo mensaje de {direccion}: {mensaje}\n'.encode('utf-8')
                    transmision(mensaje_a_transmitir, cliente)
            else:
                # si no hay datos, desconectar al cliente
                cliente.close()
                clientes.remove(cliente)
                transmision(f'Cliente {direccion} se ha desconectado.\n'.encode('utf-8'))
                break
        except:
            # si ocurre un error, desconectar al cliente
            cliente.close()
            clientes.remove(cliente)
            transmision(f'Cliente {direccion} se ha desconectado.\n'.encode('utf-8'))
            break

# socket del servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, port))
servidor.listen(5)
print(f'Servidor escuchando en {host}:{port}')

# aceptar conexiones entrantes y crear hilos para manejar a los clientes
while True:
    cliente, direccion = servidor.accept()
    print(f'Nueva conexión de {direccion}')
    clientes.append(cliente)
    transmision(f'Cliente {direccion} se ha conectado.\n'.encode('utf-8'))
    cliente_thread = threading.Thread(target=manejar_cliente, args=(cliente, direccion))
    cliente_thread.start()
