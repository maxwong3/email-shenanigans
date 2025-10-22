from socket import *
import os

def main():
    host = '127.0.0.1'
    port = 110
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((host, port))
    server.listen(3)
    print(f"POP3 server running on port {port}")
    while True:
        conn, addr = server.accept()
        handle_pop3(conn, addr)

def handle_pop3(conn, addr):
    print(f"POP3 connection from {addr}")
    conn.send(b"+OK POP3 server ready\r\n")

    user = None
    mail_dir = None
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mail_root = os.path.join(base_dir, "..", "saved_mail")

    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break
        print("C:", data)

        parts = data.split()
        if len(parts) == 0:
            continue

        cmd = parts[0].upper()

        if cmd == "USER" and len(parts) == 2:
            user = parts[1]
            mail_dir = os.path.join(mail_root, user)
            if not os.path.exists(mail_dir):
                os.makedirs(mail_dir)
            conn.send(b"+OK user accepted\r\n")

        elif cmd == "PASS":
            # No authentication implemented currently
            conn.send(b"+OK login successful\r\n")

        elif cmd == "LIST":
            if not user or not mail_dir:
                conn.send(b"-ERR must log in first\r\n")
                continue
            if not os.path.exists(mail_dir):
                os.makedirs(mail_dir)
            files = os.listdir(mail_dir)
            response = [f"+OK {len(files)} messages"]
            for i, f in enumerate(files, 1):
                size = os.path.getsize(os.path.join(mail_dir, f))
                response.append(f"{i} {size}")
            response.append(".")
            conn.send(("\r\n".join(response) + "\r\n").encode())

        elif cmd == "RETR" and len(parts) == 2:
            index = int(parts[1]) - 1
            if not os.path.exists(mail_dir):
                os.makedirs(mail_dir)
            files = sorted(os.listdir(mail_dir))
            if 0 <= index < len(files):
                filepath = os.path.join(mail_dir, files[index])
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                conn.send(b"+OK message follows\r\n")
                conn.send(content.encode() + b"\r\n.\r\n")
            else:
                conn.send(b"-ERR no such message\r\n")

        elif cmd == "QUIT":
            conn.send(b"+OK quit\r\n")
            conn.close()
            return

        else:
            conn.send(b"-ERR unknown command\r\n")

if __name__ == "__main__":
    main()
