# Лабораторная работа "Docker: докеризация приложения"
## Задание
Собрать из исходного кода и запустить в докере рабочее приложение с базой данных.
1. Образ должен быть легковесным
2. Использовать базовые легковесные образы - alpine
3. Вся конфигурация приложения должна быть через переменные окружения
4. Статика (зависимости) должна быть внешним томом `volume`
5. Создать файл `docker-compose` для старта и сборки
6. В `docker-compose` нужно использовать базу данных
7. При старте приложения должно быть учтено выполнение автоматических миграций
8. Контейнер должен запускаться от непривилегированного пользователя
9. После установки всех нужных утилит, должен очищаться кеш

## Выполнение работы
1. Создание приложения

- В качестве простого приложения решено написать сайт, на котором отображается база данных пользователей:
логин пользователя и его пароль (все максимально безопасно, конечно же 🙂).

- Написано приложение на python с использованием фреймворка Flask. На странице можно удалить запись из таблицы, а также 
добавить новую запись. В качестве ORM используется SQLAlchemy, диалект БД - Postgres. Представлено в файлах app.py,
index.html и styles.css.

2. Действия до создания докера

- Все переменные окружения вынесены в отдельный файл .env:
```
POSTGRES_HOST=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=12345
POSTGRES_DB=flask_db
SECRET_KEY=secret
```
- Они используются при конфигурации приложения app.py и непосредственно в docker-compose.yml 

3. Создание Dockerfile:
- Файл Dockerfile имеет следующий вид:
```
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
```
- Комментарии даны в коде, но стоит указать, что в качестве базового образа используется легковесный `python:3.12.2-alpine`. 
Новый пользователь создается для непривилегированного запуска контейнера. Затем устанавливаются 
необходимые библиотеки, после чего происходит чистка кэша. Копируются исходные файлы с миграциями и указывается порт работы
приложения. В конце указывается точка входа.

4. Точка входа
- По запуску контейнера выполняется bash-скрипт entrypoint.sh, в котором выполняются миграции базы данных и запуск приложения:
```
#!/bin/sh
python3 -m flask db init
python3 -m flask db migrate
python3 -m flask db upgrade
python3 app.py
```

5. docker-compose.yml
- Рассмотрим структуру файла:
```
services:
  db:
   image: postgres  # образ БД постгрес
   environment:
     POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
     POSTGRES_USER: ${POSTGRES_USER}
     POSTGRES_DB: ${POSTGRES_DB}
   ports:
     - "5432:5432"
   volumes:
     - postgres-data:/var/lib/postgresql/data  # том для хранения данных БД
   networks:
     - docker_network

  app:
    build: .
    container_name: flask_app
    environment:
      POSTGRES_HOST: ${POSTGRES_HOST}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_DB: ${POSTGRES_DB}
      SECRET_KEY: ${SECRET_KEY}  # секретный ключ Flask-приложения
    depends_on: # запустить БД до приложения
      - db
    ports:
      - "8000:8000"
    networks:
      - docker_network

volumes:
  postgres-data:
    driver: local

networks:
  docker_network:
    driver: bridge  # используем сетевой драйвер "bridge" для внутренней сети Docker
```
В этом файле описываются два сервиса: db (для базы данных PostgreSQL) и app (для приложения).

- db: Используется Docker-образ Postgres для запуска базы данных. Затем задаются переменные окружения из файла .env и
на хосте открывается порт 5432, который пробрасывается в контейнер. Создается том postgres-data (`volume`), который сохраняет данные бд.


- app: Контейнер, запускающий приложение. Он пробрасывает порт 5000 на хосте и связывает со своим. С помощью параметра 
depends_on мы можем гарантировать, что база данных будет запущена перед приложением. Приложение подключилось к сети docker_network, 
что позволяет ему взаимодействовать с другими сервисами в пределах этой сети.

6. Запуск докера
- Для начала с целью запуска демона докера запускается приложение Docker Desktop.
- Затем в корневой директории проекта выполняется команда:
```
docker compose up --build -d
```
- После ее запуска сбилдится образ и запустятся два контейнера. Это можно проверить командой:
```
docker ps
```
![alt text](https://github.com/mx-tsr/seti-lab4-docker/blob/main/1.png?raw=true)

7. Вес образа
- После сборки вес образа составляет: 153MB

8. Демонстрация работы

![alt text](https://github.com/mx-tsr/seti-lab4-docker/blob/main/2.png?raw=true)

![alt text](https://github.com/mx-tsr/seti-lab4-docker/blob/main/3.png?raw=true)

![alt text](https://github.com/mx-tsr/seti-lab4-docker/blob/main/4.png?raw=true)