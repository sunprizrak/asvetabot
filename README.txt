1. git clone https://github.com/sunprizrak/asvetabot.git
2. cd asvetabot

# При первом получении сертификата ssl
    1) chmod +x init-letsencrypt.sh
    2) sudo ./init-letsencrypt.sh
    3) docker compose down
#--- end ---#

3. docker compose up -d



# Команды докера
docker compose up -d # Команда для запуска контейнера
docker compose down # Команда для остановки контейнера
docker image prune # Удаляет старые image