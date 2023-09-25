using System.Net.Sockets;
using System.Text;

class Cliente
{
    static void Main()
    {
        Console.Write("*** BIENVENIDO AL CLIENTE EN LENGUAJE C# ***\n");
        string nombreUsuario = "";
        while (string.IsNullOrWhiteSpace(nombreUsuario))
        {
            Console.Write(">> Ingresa tu nombre de usuario: ");
            nombreUsuario = Console.ReadLine();

            if (string.IsNullOrWhiteSpace(nombreUsuario))
            {
                Console.WriteLine("El nombre de usuario no puede estar vacío. Por favor, ingresa un nombre de usuario válido.");
            }
        }
        // Configurar el socket del cliente
        TcpClient cliente = new TcpClient();
        Console.Write("Ingresa la dirección IP del servidor: ");
        string servidorIP = Console.ReadLine();
        Console.Write("Ingresa el puerto del servidor: ");
        int servidorPuerto = int.Parse(Console.ReadLine());

        try
        {
            cliente.Connect(servidorIP, servidorPuerto);

            // Comprobar si la conexión fue exitosa
            if (cliente.Connected)
            {
                Console.WriteLine("Conexión exitosa al servidor \n\n");
            }
            else // Salir si la conexión no fue exitosa
            {
                Console.WriteLine("No se pudo establecer la conexión al servidor.");
                return; 
            }

            // Iniciar un hilo para recibir mensajes
            Thread threadRecv = new Thread(() => RecibirMensajes(cliente));
            threadRecv.Start();

            while (true)
            {
                Console.WriteLine("**ESCRIBE UN MENSAJE**");
                string mensaje = Console.ReadLine();

                if (!string.IsNullOrWhiteSpace(mensaje))
                {
                    if (mensaje == "/listar" || mensaje == "/quitar")
                    {
                        EnviarMensaje(cliente, mensaje);
                        if (mensaje == "/quitar")
                            break;
                    }
                    else
                    {
                        EnviarMensaje(cliente, $"{nombreUsuario}: {mensaje}");
                    }
                }
                else
                {
                    Console.WriteLine("No puedes enviar un mensaje vacío. Escribe algo.");
                }
            }

            // Cerrar el socket del cliente
            cliente.Close();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error: {ex.Message}");
        }
    }

    static void RecibirMensajes(TcpClient cliente)
    {
        try
        {
            NetworkStream stream = cliente.GetStream();
            byte[] buffer = new byte[1024];

            while (true)
            {
                int bytesRead = stream.Read(buffer, 0, buffer.Length);
                if (bytesRead > 0)
                {
                    string mensaje = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                    Console.WriteLine(mensaje);
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error al recibir mensajes: {ex.Message}");
        }
    }

    static void EnviarMensaje(TcpClient cliente, string mensaje)
    {
        try
        {
            NetworkStream stream = cliente.GetStream();
            byte[] buffer = Encoding.UTF8.GetBytes(mensaje);
            stream.Write(buffer, 0, buffer.Length);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error al enviar mensaje: {ex.Message}");
        }
    }
}
