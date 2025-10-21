from socket import *

def main():
    server_host = '127.0.0.1'
    server_port = 2525
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(3)
    print(f"Server ready to receive on port {server_port}")
    while True:
        connection_socket, addr = server_socket.accept()
        handle_commands(connection_socket, addr)

def handle_commands(conn, addr):
    print(f"Connected by {addr}")
    conn.send(b"220 SimpleSMTPServer Ready\r\n")

    data_buffer = ""
    sending_data = False
    lines = []
    while True:
        command = conn.recv(1024)
        if not command:
            break
        data_buffer += command.decode()

        while "\r\n" in data_buffer:
            line, data_buffer = data_buffer.split("\r\n", 1)
            print("C:", line)

            # When client has started sending the message data
            if sending_data == True:
                if line == ".": 
                    print("📧 Received email:")
                    print("\n".join(lines))
                    conn.send(b"250 OK: Message accepted\r\n")
                    sending_data = False
                    lines.clear()
                else:
                    lines.append(line)
                continue

            cmd = line.upper()
            if cmd.startswith("HELO") or cmd.startswith("EHLO"):
                conn.send(b"250 Hello\r\n")
            elif cmd.startswith("MAIL FROM:"):
                conn.send(b"250 OK\r\n")
                mail_from = line[10:].strip()
            elif cmd.startswith("RCPT TO:"):
                conn.send(b"250 OK\r\n")
                rcpt_to = line[8:].strip()
            elif cmd.startswith("DATA"):
                conn.send(b"354 END DATA WITH <CR><LF>.<CR><LF>\r\n")
                sending_data = True
            elif cmd.startswith("QUIT"):
                conn.send(b"221 OK\r\n")
                conn.close()
                return
            else:
                conn.send(b"502 Command not implemented\r\n")

if __name__ == "__main__":
    main()