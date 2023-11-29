import smtplib
from email.message import EmailMessage


async def send_email(data):
    msg = EmailMessage()
    msg.set_content(data)

    msg['Subject'] = 'FSM Data'
    msg['From'] = 'your_email@example.com'  # Замените на вашу электронную почту
    msg['To'] = 'recipient@example.com'  # Замените на адрес получателя

    # Настройте SMTP сервер и отправьте письмо
    with smtplib.SMTP(host='smtp.example.com', port=587) as smtp:  # Замените на данные вашего SMTP сервера
        smtp.starttls()

        smtp.login(
            user='sunprizrak@gmail.com',
            password='')

        smtp.send_message(msg)
