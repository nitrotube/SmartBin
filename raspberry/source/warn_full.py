import smtplib
from email.mime.text import MIMEText

def send_warn_full(type):
    server_addr  = 'smtp.timeweb.ru'
    port = 2525
    pi_login = 'warning@smartbin.ru'
    pi_pass = 'warning12'
    to = 'e.spirin@smartbin.ru'

    body = '<h1 color = "red" font = "Times New Roman">The bin is full of ' + type + ' </h1>'
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
