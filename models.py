
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True)

    password = db.Column(db.String(255))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Profile(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100))

    profession = db.Column(db.String(100))

    about = db.Column(db.Text)

    email = db.Column(db.String(100))

    phone = db.Column(db.String(30))

    photo = db.Column(db.String(255))


class Project(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))

    description = db.Column(db.Text)

    image = db.Column(db.String(255))

    github = db.Column(db.String(255))

    demo = db.Column(db.String(255))

    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow)


class Contact(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100))

    subject = db.Column(db.String(200))

    message = db.Column(db.Text)

    created_at = db.Column(db.DateTime,
                           default=datetime.utcnow)