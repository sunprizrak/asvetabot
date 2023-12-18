import os
import datetime
import smtplib
from email.message import EmailMessage
from bot import get_bot
from config_reader import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


async def send_email(data):
    if data.get('doc'):
        bot = get_bot()

        msg = MIMEMultipart()

        msg.attach(MIMEText(data['text']))

        if not os.path.exists('download'):
            os.mkdir('download')

        for doc_data in data['doc']:

            content = await bot.download_file(doc_data[list(doc_data)[0]])

            with open(os.path.join('download', list(doc_data)[0]), 'wb') as file:
                file.write(content.getvalue())

            with open(os.path.join('download', list(doc_data)[0]), "rb") as doc_file:
                doc_part = MIMEApplication(doc_file.read(), Name=list(doc_data)[0])
                doc_part['Content-Disposition'] = f'attachment; filename={list(doc_data)[0]}'
                msg.attach(doc_part)

            if os.path.exists(os.path.join('download', list(doc_data)[0])):
                os.remove(os.path.join('download', list(doc_data)[0]))
    else:
        msg = EmailMessage()
        msg.set_content(data['text'])

    msg['Subject'] = '[Asveta TgBot] Анкета от ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    msg['From'] = config.email_user
    msg['To'] = config.email_to

    with smtplib.SMTP(host=config.email_host, port=config.email_port) as smtp:
        smtp.starttls()

        smtp.login(
            user=config.email_user,
            password=config.email_pass.get_secret_value())

        smtp.send_message(msg)

    return True


