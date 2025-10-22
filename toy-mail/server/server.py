from socket import *
import os 
from datetime import datetime

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

    base_dir = os.path.dirname(os.path.abspath(__file__))
    mail_dir = os.path.join(base_dir, "..", "saved_mail")
    os.makedirs(mail_dir, exist_ok=True)

    sender_email=None
    recipient_email = None
    while True:
        command = conn.recv(1024)
        if not command:
            break
        data_buffer += command.decode()
        print("TESTING data_buffer:", data_buffer, "\n")

        while "\r\n" in data_buffer:
            line, data_buffer = data_buffer.split("\r\n", 1)
            print("C:", line)

            # When client has started sending the message data
            if sending_data == True:
                if line == ".": 
                    print("📧 Received email:")
                    print("\n".join(lines))
                    # Tell client email has been succesfully accepted and stored
                    conn.send(b"250 OK: Message accepted\r\n")
                    sending_data = False

                    if recipient_email:
                        recipient_dir = os.path.join(mail_dir, recipient_email)
                        recipient_dir = recipient_dir.replace("<", "")
                        recipient_dir = recipient_dir.replace(">", "")
                        os.makedirs(recipient_dir, exist_ok=True)

                        # lines.insert(0, f"Subject: (Subject not provided by header)")
                        # lines.insert(0, f"To: {recipient_email}")
                        # lines.insert(0, f"From: {sender_email}")

                        # Save to file
                        date_format = "%Y-%m-%d_%H-%M-%S"
                        filename = "email-" + datetime.now().strftime(date_format) + ".txt"
                        filepath = os.path.join(recipient_dir, filename)
                        with open(filepath, "w", encoding="utf-8") as f:
                            for line in lines:
                                f.write(line + "\n")

                        print(f"Message received and forwarded to local mailbox: {recipient_email}")
                        lines.clear()
                else:
                    lines.append(line)
                continue

            cmd = line.upper()
            if cmd.startswith("HELO") or cmd.startswith("EHLO"):
                conn.send(b"250 Hello\r\n")
            elif cmd.startswith("MAIL FROM:"):
                conn.send(b"250 OK\r\n")
                sender_email = line[10:].strip()
            elif cmd.startswith("RCPT TO:"):
                conn.send(b"250 OK\r\n")
                recipient_email = line[8:].strip()
            elif cmd.startswith("DATA"):
                conn.send(b"354 OK\r\n")
                sending_data = True
            elif cmd.startswith("QUIT"):
                conn.send(b"221 OK\r\n")
                conn.close()
                return
            else:
                conn.send(b"502 Command not implemented\r\n")

if __name__ == "__main__":
    main()