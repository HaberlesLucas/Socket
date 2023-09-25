import socket
import threading # para crear hilos 

# ip y puerto del servidor 
host = '127.0.0.1' 
port = 1812     

#para almacenar los clientes conectados
clientes = []

#f para manejar la comunicación con un cliente
def manejar_cliente(cliente, direccion):
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            if mensaje:
                if mensaje == "/listar":
                    #enviar la lista de usuarios conectados al cliente que la solicita
                    lista_usuarios = ", ".join([str(c.getpeername()) for c in clientes])
                    cliente.send(f'Usuarios conectados: {lista_usuarios}'.encode('utf-8'))
                elif mensaje == "/quitar":
                    #desconectar al cliente que envía el comando "/quitar"
                    cliente.close()
                    clientes.remove(cliente)
                    break
                else:
                    #reenviar el mensaje a todos los clientes
                    
                    #'{mensaje} contiene en name_user y mensaje => 'Nuevo mensaje de {mensaje}' mostrará una 
                    # salida como >> "Nuevo mensaje de Lucas: contenido del mensaje"
                    mensaje_a_transmitir = f'Nuevo mensaje de {mensaje}' 
                    for c in clientes:
                        if c != cliente:
                            c.send(mensaje_a_transmitir.encode('utf-8'))
            else:
                #si no hay datos, desconectar al cliente
                cliente.close()
                clientes.remove(cliente)
                break
        except:
            #si ocurre un error, desconectar al cliente
            cliente.close()
            clientes.remove(cliente)
            break


#socket del servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, port))
servidor.listen(5)
print(f'Servidor escuchando en {host}:{port}')

#aceptar conexiones entrantes y crear hilos para manejar a los clientes
while True:
    cliente, direccion = servidor.accept()
    print(f'Nueva conexión de {direccion}')
    clientes.append(cliente)
    cliente_thread = threading.Thread(target=manejar_cliente, args=(cliente, direccion))
    cliente_thread.start()