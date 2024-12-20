import os
from dotenv import load_dotenv

load_dotenv('../.env')
print(os.environ.get('POSTGRES_USER'))

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://{USER}:{PASSWORD}@{DB_HOST}:5432/{DB_NAME}".format(
        USER=os.environ.get("POSTGRES_USER"),
        PASSWORD=os.environ.get("POSTGRES_PASSWORD"),
        DB_HOST=os.environ.get("POSTGRES_HOST"),
        DB_NAME=os.environ.get("POSTGRES_DB")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # не будет сигнализировать каждый раз, когда в бд должно быть внесено изменение
    SECRET_KEY = os.environ.get("SECRET_KEY")