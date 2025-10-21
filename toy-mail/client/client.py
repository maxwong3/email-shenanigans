from socket import *
import smtplib
from email.message import EmailMessage

def main():
    smtp_host = '127.0.0.1'
    smtp_port = 2525

    msg = EmailMessage()
    msg['From'] = 'sender@example.com'
    msg['To'] = 'receiver@example.com'
    msg['Subject'] = 'Test email 2'
    msg.set_content("Hello receiver, \n\nI have a project due tonight.\nPlease send help.\nI don't have much time to spare please.\n\nSender")

    smtp = smtplib.SMTP(smtp_host, smtp_port)
    smtp.send_message(msg)

if __name__ == "__main__":
    main()