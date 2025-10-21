from socket import *
def main():
    server_name = 'localhost'
    server_port = 2525
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))

    greeting = client_socket.recv(1024).decode().strip()
    print(f"S: {greeting}")

    # Example SMTP connection
    send_command(client_socket, "FAKE command")
    send_command(client_socket, "HELO maw564@pitt.edu")

    client_socket.close()

def send_command(socket, cmd):
    print(f"C: {cmd}")
    command = cmd + "\r\n"
    socket.send(command.encode())
    response = socket.recv(1024)
    print(f"S: {response.decode()}")

if __name__ == "__main__":
    main()