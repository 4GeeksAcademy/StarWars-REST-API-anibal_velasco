from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine


db = SQLAlchemy()

class User(db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Planetas(db.Model):
    __tablename__ = 'planetas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def __init__(self,name):
        self.name = name
    
    def __repr__(self):
        return f'<planeta name:{self.name}>'
    
    def serialize(self):
        return{
            "id":self.id,
            "name": self.name
        }


class Personajes(db.Model):
    __tablename__ = 'personajes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    def __init__(self,name):
        self.name = name
    
    def __repr__(self):
        return f'<Personaje name:{self.name}>'
    
    def serialize(self):
        return{
            "id":self.id,
            "name": self.name
        }



class Planetas_favoritos(db.Model):
    __tablename__ = 'planetas_favoritos'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship(User, backref = 'todos_los_planetas_favoritos')

    planeta_id = db.Column(db.Integer, db.ForeignKey('planetas.id'))
    planeta = relationship(Planetas)


class Personajes_favoritos(db.Model):
    __tablename__ = 'personajes_favoritos'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship(User, backref = 'todos_los_Personajes_favoritos')

    personaje_id = db.Column(db.Integer, db.ForeignKey('personajes.id'))
    personaje = relationship(Personajes)