# CS1652 Project 1 Email System Documentation

## Project Overview

Email client server system with SMTP and POP3 protocol implementation

### Running the project
- Python 3.11
- Anaconda VM 
```
py toy-mail/server/server.py
py toy-mail/server/pop3_server.py
py toy-mail/client/client.py
```

### SMTP

Commands implemented:
- HELO
- MAIL FROM
- RCPT TO
- DATA
- QUIT

Protocol Flow

```
C: HELO client
S: 250 Hello
C: MAIL FROM:<sender@example.com>
S: 250 OK
C: RCPT TO:<receiver@example.com>
S: 250 OK
C: DATA
S: 354
C: <email body>
C: .
S: 250 OK: Message accepted
C: QUIT
S: 221 OK
```


### POP3

Commands implemented:
- USER
- PASS (not really)
- LIST
- RETR
- QUIT

```
C: USER receiver@example.com
S: +OK user accepted
C: PASS password
S: +OK login successful
C: LIST
S: +OK 1 messages
S: 1 356
S: .
C: RETR 1
S: +OK message follows
<email content>
.
C: QUIT
S: +OK quit
```

### server.py
Establishes SMTP server. Runs and listens to clients that may connect to the server, then sending a series of SMTP commands until it QUITS. Logic of this handling of commands found in handle_commands(). Commands such as HELO,
MAIL FROM, RCPT TO all return a response code of 250 back to the client over this connection when the commands are sent. The data command sends all the actual data from the email to the recipient. This is handled by
the if statement sending_data == True. The email contents are stored in a new text file stored locally and in a directory corresponding to the recipient. The email would be forwarded over to the recipient client in this way.
Lastly, the QUIT command exits the connection.

### client.py
Client script that connects to the server to send emails. It also can read emails with the pop3 protocol and server implementation. After prompting the user for their email address, the email address/user can either 
send or read emails. For sending emails, it establishes a connection to the SMTP server. Using EmailMessage, the client input email headers and message and the message is sent over via one send_message call. But as the headers
(sender, recipient) and message is being input and set, the commands are being called over this connection. In the inbox() function, it handles reading of the emails. As SMTP doesn't really allow you to read emails, I used
POP3 for this. It connects to the pop3 server (pop3_server.py) and in this instance just gets the length of list and calls retr commands to view the client's inbox.

### pop3_server.py
Establishes a POP3 server, the core function implemented is handle_pop3, which handles pop3 commands sent by the client. The script gets the email contents from the directory path of the user, its contents saved locally.
Command USER establishes the connected user and returns an +OK response code (along with every command except for when errors occur (-ERR response code). As a defensive programming tactic, I create the directory if it doesn't
exist of the user here. PASS command is included as its one of the core commands in POP3, but is not implemented. LIST returns a list of emails in the recipient inbox and their sizes, RETR retrieves a specific email.
