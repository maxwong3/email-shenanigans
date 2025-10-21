from socket import *
import smtplib
from email.message import EmailMessage

def main():
    smtp_host = '127.0.0.1'
    smtp_port = 2525

    msg = EmailMessage()
    msg['From'] = 'sender@example.com'
    msg['To'] = 'receiver@example.com'
    msg['Subject'] = 'Test email'
    msg.set_content("Hello receiver, \n\nHope you're doing well.\nBecause I sure ain't.\n(Just kidding)\n\nSender")

    smtp = smtplib.SMTP(smtp_host, smtp_port)
    smtp.set_debuglevel(1)
    smtp.send_message(msg)

if __name__ == "__main__":
    main()