import smtplib
from email.message import EmailMessage
def send_email(email_,message_):
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login('Y.ghazali1693@gmail.com','ghazali1478')
    msg = EmailMessage()
    msg.set_content(message_)
    msg['Subject']='Password reset'
    msg['From']='Y.ghazali1693@gmail.com'
    msg['To']=email_
    server.sendmail('Y.ghazali1693@gmail.com',email_,msg.as_string())
    server.quit()