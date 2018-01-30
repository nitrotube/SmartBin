import smtplib
from email.mime.text import MIMEText

def send_warn_full():
    server_addr  = 'smtp.gmail.com'
    port = 587
    pi_login = 'smartbin.warner'
    pi_pass = 'sbwarner2018'
    to = 'e.spirin@smartbin.ru'

    body = '<h1 color = "red" font = "Times New Roman">Musorka zabita</h1>'
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

if __name__=='__main__':
    send_warn_full()
