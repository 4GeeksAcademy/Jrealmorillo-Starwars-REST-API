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
from models import db, User, People, Planet, Favorite
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


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    serialized_users = [{'id': user.id, 'name': user.name} for user in users]
    return jsonify(serialized_users)


@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    serialized_people = [person.serialize() for person in people]
    return jsonify(serialized_people)


@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person:
        serialized_person = person.serialize()
        return jsonify(serialized_person)
    else:
        return jsonify({'message': 'Person not found'}), 404


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    serialized_planets = [planet.serialize() for planet in planets]
    return jsonify(serialized_planets)


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        serialized_planet = planet.serialize()
        return jsonify(serialized_planet)
    else:
        return jsonify({'message': 'Planet not found'}), 404

    
   
@app.route('/users/<int:user_id>/favorites/', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if user:
        favorites = user.favorites
        serialized_favorites = []
        for favorite in favorites:
            if favorite.planet_id:
                serialized_favorites.append({
                    'id': favorite.id,
                    'type': 'planet',
                    'planet_id': favorite.planet_id
                })
            elif favorite.people_id:
                serialized_favorites.append({
                    'id': favorite.id,
                    'type': 'people',
                    'people_id': favorite.people_id
                })
        return jsonify(serialized_favorites)
    else:
        return jsonify({'message': 'User not found'}), 404
    


@app.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=['POST'])
def add_favorite_planet(planet_id, user_id):
    user = User.query.get(user_id)
    if user:
        favorite = Favorite(user_id=user.id, planet_id=planet_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'message': 'Favorite planet added successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/favorite/people/<int:people_id>/<int:user_id>', methods=['POST'])
def add_favorite_people(people_id, user_id):
    user = User.query.get(user_id)
    if user:
        favorite = Favorite(user_id=user.id, people_id=people_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'message': 'Favorite people added successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id, user_id):
    user = User.query.get(user_id)
    if user:
        favorite = Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({'message': 'Favorite planet deleted successfully'})
        else:
            return jsonify({'message': 'Favorite planet not found'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/favorite/people/<int:people_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_people(people_id, user_id):
    user = User.query.get(user_id)
    if user:
        favorite = Favorite.query.filter_by(user_id=user.id, people_id=people_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({'message': 'Favorite people deleted successfully'})
        else:
            return jsonify({'message': 'Favorite people not found'}), 404
    else:
        return jsonify({'message': 'User not found'}), 404



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
