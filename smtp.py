import os
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

        for doc_data in data['doc']:

            content = await bot.download_file(doc_data[list(doc_data)[0]])

            # Сохраняем содержимое файла в указанную директорию
            with open(os.path.join('./download', list(doc_data)[0]), 'wb') as file:
                file.write(content.getvalue())  # Сохраняем содержимое файла

            with open(os.path.join('./download', list(doc_data)[0]), "rb") as doc_file:
                doc_part = MIMEApplication(doc_file.read(), Name=list(doc_data)[0])
                doc_part['Content-Disposition'] = f'attachment; filename={list(doc_data)[0]}'
                msg.attach(doc_part)
    else:
        msg = EmailMessage()
        msg.set_content(data['text'])

    msg['Subject'] = 'tg @asveta.by'
    msg['From'] = config.email_user
    msg['To'] = 'sunprizrak@gmail.com'

    with smtplib.SMTP(host=config.email_host, port=config.email_port) as smtp:
        smtp.starttls()

        smtp.login(
            user=config.email_user,
            password=config.email_pass.get_secret_value())

        smtp.send_message(msg)

    return True


# async def send_document_by_email(document_path, recipient_email, smtp_server, smtp_port, smtp_username, smtp_password):
#     # Создаем объект MIMEMultipart
#     msg = MIMEMultipart()
#
#     # Добавляем текстовое сообщение
#
#
#     # Читаем содержимое файла документа
#
#
#     # Добавляем документ к сообщению
#     msg.attach(document_part)
#
#     # Настраиваем параметры SMTP-сервера
#     smtp_server = smtplib.SMTP(smtp_server, smtp_port)
#     smtp_server.starttls()
#     smtp_server.login(smtp_username, smtp_password)
#
#     # Отправляем сообщение
#     smtp_server.sendmail(smtp_username, recipient_email, msg.as_string())
#
#     # Завершаем соединение с SMTP-сервером
#     smtp_server.quit()

