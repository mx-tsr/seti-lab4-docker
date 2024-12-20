from flask import Flask, render_template, request, redirect, url_for  # для сервера
from flask_sqlalchemy import SQLAlchemy  # для ORM
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)

# Конфигурация базы данных
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:12345@localhost:5432/flask_db')
app.config.from_object(Config)

# Инициализация базы данных и миграций
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


@app.route('/')
def index():
    data = User.query.all()
    return render_template('index.html', data=data)

@app.route('/create', methods=["POST"])
def create():
    name = request.form['name']
    password = request.form['password']
    newUser = User(name=name, password=password)
    db.session.add(newUser)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete', methods=["POST"])
def delete():
    userID = request.form['id']
    if userID.isdigit():
        user = User.query.get(int(userID))
        if user:
            db.session.delete(user)
            db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
