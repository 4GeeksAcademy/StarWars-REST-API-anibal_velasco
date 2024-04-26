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
from models import db, User, Planetas, Personajes, Favoritos
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
#from models import Person

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
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
    
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def agregar_planeta_favorito(planet_id):
    # Obtener el usuario actual (puedes ajustar esta lógica según tu aplicación)
    user_id = 1  # Suponiendo que el usuario actual tiene el ID 1
    
    # Buscar al usuario en la base de datos
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    # Buscar el planeta en la base de datos
    planeta = Planetas.query.get(planet_id)
    if planeta is None:
        return jsonify({'error': 'Planeta no encontrado'}), 404

    # Crear un nuevo favorito y asociarlo al usuario y al planeta
    favorito = Favoritos(user_id=user.id, planeta_id=planeta.id)
    db.session.add(favorito)
    db.session.commit()

    return jsonify({'message': f'Planeta {planeta.name} agregado a favoritos del usuario {user.name}'}), 200
        
#PLANETAS

#PERSONAJES
@app.route('/personajes', methods=['GET'])
def get_personajes():

    personajes = Personajes.query.all()

    response_body = [item.serialize() for item in personajes]

    return jsonify(response_body), 200


@app.route('/personaje/<int:personaje_id>', methods=['GET'])
def get_personaje(personaje_id):
    personaje = Personajes.query.get(personaje_id)

    if personaje:
        return jsonify(personaje.serialize()), 200
    else:
        return jsonify({'message': 'Usuario no encontrado'}), 404
#PERSONAJES


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    # Query your database for email and password
    user = User.query.filter_by(email=email, password=password).first()

    if user is None:
        # The user was not found on the database
        return jsonify({"msg": "Bad email or password"}), 401
    
    # Create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })


@app.route("/user/favorite", methods=["GET"])
@jwt_required()
def user_favorite():
    current_user = get_jwt_identity()
    if current_user:
        user_filter = User.query.filter_by(email=current_user).first()
        if user_filter:
            return jsonify(user_filter.serialize()), 200
        else:
            return jsonify({"message": "User not found"}), 404
    else:
        return jsonify({"message": "User identity not found"}), 400



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
