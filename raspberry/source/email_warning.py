import smtplib
from email.mime.text import MIMEText
from config import EMAIL


def send_warn_full():
    server_addr  = EMAIL["server"]
    port = int(EMAIL["port"])
    pi_login = EMAIL["login"]
    pi_pass = EMAIL["password"]
    to = EMAIL["to"]

    body = '<h1 color = "red" font = "Times New Roman">The bin is full of sheet </h1>'
    title = 'SBWarning'
    msg = MIMEText((body),'html')

    msg['From'] = 'SBWarner'
    msg['To'] = 'Somebody'
    msg['Subject'] = title
    message = msg.as_string()

    server = smtplib.SMTP(server_addr, port)
    server.starttls()
    server.login(pi_login, pi_pass)
    server.sendmail(pi_login, to, message)
    server.quit()
