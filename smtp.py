import smtplib
from email.message import EmailMessage
from config_reader import config
import json


async def send_email(data):
    msg = EmailMessage()
    msg.set_content(data)

    msg['Subject'] = 'FSM Data'
    msg['From'] = config.email_user
    msg['To'] = 'sunprizrak@gmail.com'

    with smtplib.SMTP(host=config.email_host, port=config.email_port) as smtp:
        smtp.starttls()

        smtp.login(
            user=config.email_user,
            password=config.email_pass.get_secret_value())

        smtp.send_message(msg)
