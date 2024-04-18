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
            "personajes_favoritos": [item.serialize() for item in self.todos_los_favoritos]
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



class Favoritos(db.Model):
    __tablename__ = 'favoritos'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship(User, backref = 'todos_los_favoritos')

    planeta_id = db.Column(db.Integer, db.ForeignKey('planetas.id'))
    planeta = relationship(Planetas)

    personaje_id = db.Column(db.Integer, db.ForeignKey('personajes.id'))
    personaje = relationship(Personajes)


    def serialize(self):
        return{
            "id":self.id,
            "planeta": self.planeta.serialize() if self.planeta else ""  ,
            "personaje":self.personaje.serialize() if self.personaje else "" 
        }

    # tabla_de_asociaciones = db.table(
    #     "tabla_de_asociaciones",
    #     db.metadata,
    #     db.column()
    #     db.column()
    # )