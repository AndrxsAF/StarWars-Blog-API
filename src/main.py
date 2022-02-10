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
from models import db, User, Planet, People, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

# functions for planet

# functions to show the user database

@app.route('/user', methods=['GET'])
def show_users():
    users = User.query.all()
    return jsonify(list(map(lambda tasks: tasks.serialize(), users))), 200

# functions to add a new user to database
    
@app.route('/user/add', methods=['POST'])
def add_users():
    body = request.get_json()
    new_user = User(username=body["username"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 200

# functions to show or delete an user from the database

@app.route('/user/<id>', methods=['GET', 'DELETE'])
def delete_users(id):
    user = User.query.get(id)
    if user:
        if request.method == "GET":
            return jsonify(user.serialize())
        elif request.method == "DELETE":
            db.session.delete(user)
            db.session.commit()
            return jsonify('User deleted successfuly.')
    else:
        return jsonify('No existe esa función')

# functions for favorites

# functions to add and delete a planet in favorites

@app.route('/user/<id>/favorites/planet/<planetID>', methods=['POST', 'DELETE'])
def add_favorite_planet(id, planetID):
    if request.method == "POST":
        new_favorite = Favorite(userID = id, planetID = planetID, peopleID = None)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(new_favorite.serialize()), 200
    elif request.method == "DELETE":
        favorites = Favorite.query.all()
        favorite_list = list(map(lambda favorite: favorite.serialize(), favorites))
        for x in favorite_list:
            if x.get('userID') == int(id) and x.get('planetID') == int(planetID):
                delete_favorite = Favorite.query.get(int(x.get('id')))
                db.session.delete(delete_favorite)
                db.session.commit()
                return jsonify(delete_favorite.serialize())    
        return jsonify('Not correct.')
    else:
        return jsonify('Only POST and DELETE methods allowed here.')

# functions to add and delete a people in favorite

@app.route('/user/<id>/favorites/people/<peopleID>', methods=['POST', 'DELETE'])
def add_favorites_people(id, peopleID):
        if request.method == "POST":
            new_favorite = Favorite(userID = id, planetID = None, peopleID = peopleID)
            db.session.add(new_favorite)
            db.session.commit()
            return jsonify(new_favorite.serialize()), 200
        elif request.method == "DELETE":
            favorites = Favorite.query.all()
            favorite_list = list(map(lambda favorite: favorite.serialize(), favorites))
            for x in favorite_list:
                if x.get('userID') == int(id) and x.get('peopleID') == int(peopleID):
                    delete_favorite = Favorite.query.get(int(x.get('id')))
                    db.session.delete(delete_favorite)
                    db.session.commit()
                    return jsonify(delete_favorite.serialize())
            return jsonify('Not correct.')
        else:
            return jsonify('Only POST and DELETE methods allowed here.')
        
# functions to show a user favorites

@app.route('/user/<id>/favorites', methods=['GET'])
def user_favorites(id):
    favorites = Favorite.query.all()
    favorite_list = list(map(lambda favorite: favorite.serialize(), favorites))
    user_favorite = []
    for x in favorite_list:
        if x.get('userID') == int(id):
            user_favorite.append(x)
    return jsonify(list(map(lambda favorite: favorite, user_favorite))), 200

# functions to show the favorite database

@app.route('/favorite', methods=['GET'])
def show_favorite():
    favorites = Favorite.query.all()
    return jsonify(list(map(lambda favorite: favorite.serialize(), favorites))), 200

# functions for planet

# functions to show the planet database

@app.route('/planet', methods=['GET'])
def show_planets():
    planets = Planet.query.all()
    return jsonify(list(map(lambda planet: planet.serialize(), planets))), 200

# functions to add a new planet to database
    
@app.route('/planet/add', methods=['POST'])
def add_planets():
    body = request.get_json()
    new_planet = Planet(name=body["name"], terrain=body["terrain"], population=body["population"])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 200

# functions to show or delete a planet from the database

@app.route('/planet/<id>', methods=['GET', 'DELETE'])
def delete_planets(id):
    planets = Planet.query.get(id)
    if planets:
        if request.method == "GET":
            return jsonify(planets.serialize())
        elif request.method == "DELETE":
            db.session.delete(planets)
            db.session.commit()
            return jsonify('Planet deleted successfuly.')
    else:
        return jsonify('No existe esa función')

# functions for people

# functions to show the people database

@app.route('/people', methods=['GET'])
def show_peoples():
    peoples = People.query.all()
    return jsonify(list(map(lambda people: people.serialize(), peoples))), 200

# functions to add a new people to database
    
@app.route('/people/add', methods=['POST'])
def add_peoples():
    body = request.get_json()
    new_people = People(name=body["name"], height=body["height"], mass=body["mass"], homeworld=body["homeworld"])
    db.session.add(new_people)
    db.session.commit()
    return jsonify(new_people.serialize()), 200

# functions to show or delete a people from the database

@app.route('/people/<id>', methods=['GET', 'DELETE'])
def delete_peoples(id):
    peoples = People.query.get(id)
    if peoples:
        if request.method == "GET":
            return jsonify(peoples.serialize())
        elif request.method == "DELETE":
            db.session.delete(peoples)
            db.session.commit()
            return jsonify('People deleted successfuly.')
    else:
        return jsonify('No existe esa función')

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
