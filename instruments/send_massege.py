import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl


def send_massage(text,user_email):
    sender_email="svitlanakohut1000@gmail.com"
    password="frkd jlpo lmna pffm"
    msg=MIMEMultipart()
    msg["From"]=sender_email
    msg["To"]=user_email
    msg["Subject"]="Код для верефікації"
    
    msg.attach(MIMEText(text,"plain"))

    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login(sender_email,password)
        server.send_message(msg)