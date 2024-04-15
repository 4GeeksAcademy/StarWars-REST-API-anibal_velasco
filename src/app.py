"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planetas, Personajes
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#USERS
@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()

    response_body = [user.serialize() for user in users]

    return jsonify(response_body), 200


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    user = User.query.get(user_id)

    if user:
        return jsonify(user.serialize()), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404
#USERS

#PLANETAS
@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planetas.query.all()

    response_body = [item.serialize() for item in planets]

    return jsonify(response_body), 200


@app.route('/planet/<int:planeta_id>', methods=['GET'])
def get_planeta(planeta_id):
    planeta = Planetas.query.get(planeta_id)

    if planeta:
        return jsonify(planeta.serialize()), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404
#PLANETAS

#PERSONAJES
@app.route('/personajes', methods=['GET'])
def get_personajes():

    personajes = Personajes.query.all()

    response_body = [item.serialize() for item in personajes]

    return jsonify(response_body), 200


@app.route('/personaje/<int:personaje_id>', methods=['GET'])
def get_planeta(personaje_id):
    personaje = Personajes.query.get(personaje_id)

    if personaje:
        return jsonify(personaje.serialize()), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404
#PERSONAJES



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
