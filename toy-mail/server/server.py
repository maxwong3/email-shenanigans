from socket import *

def main():
    server_port = 2525
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(3)
    print(f"Server ready to receive on port {server_port}")
    while True:
        connection_socket, addr = server_socket.accept()
        handle_commands(connection_socket, addr)

def handle_commands(conn, addr):
    print(f"Connected by {addr}")
    conn.send(b"220 SimpleSMTPServer Ready\r\n")

    data_buffer = ""
    while True:
        command = conn.recv(1024)
        if not command:
            break
        data_buffer += command.decode()

        while "\r\n" in data_buffer:
            line, data_buffer = data_buffer.split("\r\n", 1)
            print("C:", line)

            if line.upper().startswith("HELO"):
                conn.send(b"250 Hello\r\n")
            else:
                conn.send(b"502 Command not implemented\r\n")


if __name__ == "__main__":
    main()