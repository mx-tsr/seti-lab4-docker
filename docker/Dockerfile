# Используем легковесный базовый образ
FROM python:3.12.2-alpine

# Устанавливаем рабочий каталог
WORKDIR /docker_app

# Устанавливаем Python-зависимости
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Добавляем непривилегированного пользователя
RUN addgroup -S mx_tsr && adduser -S mx_tsr -G mx_tsr
USER mx_tsr

# Очищение кэша если это не было выполнено ранее
RUN rm -rf /var/cache/apk/*

# Копируем исходный код приложения
COPY ./src .

# Указываем переменные окружения
ENV FLASK_APP=app.py

EXPOSE 8000

# Запуск
ENTRYPOINT [ "./entrypoint.sh" ]