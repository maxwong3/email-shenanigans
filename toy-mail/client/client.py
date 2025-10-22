from socket import *
import smtplib
from email.message import EmailMessage

def send(user_email):

    
    smtp_host = '127.0.0.1'
    smtp_port = 2525

    msg = EmailMessage()
    sender = user_email
    print("New Email")
    recipient = input("To: ")
    subject = input("Subject: ")
    print("Write your message below. Enter a line with nothing but a period (.) to finish.")
    message = []
    while True:
        line = input()
        if line.strip() == ".":
            break
        message.append(line)

    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content('\n'.join(message))
    
    smtp = smtplib.SMTP(smtp_host, smtp_port)
    smtp.send_message(msg)

def inbox(user_email):
    import poplib
    
    pop3_host = "127.0.0.1"
    pop3_port = 110

    # Connect to local POP3 server
    mailbox = poplib.POP3(pop3_host, pop3_port)

    mailbox.user(user_email)
    mailbox.pass_("anything")

    # LIST
    num_messages = len(mailbox.list()[1])
    print(f"Number of messages: {num_messages}\n")

    # RETR
    for i in range(num_messages):
        response, lines, octets = mailbox.retr(i + 1)
        print(f"--- Message {i+1} ---")
        for line in lines:
            print(line.decode())
        print("-------------------\n")

    mailbox.quit()

if __name__ == "__main__":
    user = input("What's your email address: ")
    option = input("Enter 1 to send email, 2 to check inbox: ")
    if option.strip() == '1':
        send(user.strip())
    elif option.strip() == '2':
        inbox(user.strip())
    else:
        print("Invalid input.")