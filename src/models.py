from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.userID

    def serialize(self):
        return {
            "userID": self.userID,
            "username": self.username
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    planetID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    terrain = db.Column(db.String(100))
    population = db.Column(db.Integer)

    def __repr__(self):
        return '<Planet %r>' % self.planetID

    def serialize(self):
        return {
            "planetID": self.planetID,
            "name": self.name,
            "terrain": self.terrain,
            "population": self.population
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'people'
    peopleID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    homeworld = db.Column(db.Integer, db.ForeignKey('planet.planetID'))
    db.planet = db.relationship('Planet', backref='people')

    def __repr__(self):
        return '<People %r>' % self.peopleID

    def serialize(self):
        return {
            "peopleID": self.peopleID,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "homeworld": self.homeworld
            # do not serialize the password, its a security breach
        }

class Favorite(db.Model):
    __tablename__ = "favorite"
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
    planetID = db.Column(db.Integer, db.ForeignKey('planet.planetID'))
    peopleID = db.Column(db.Integer, db.ForeignKey('people.peopleID'))
    user = db.relationship('User', backref='favorite')
    planet = db.relationship('Planet', backref='favorite')
    people = db.relationship('People', backref='favorite')

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "userID": self.userID,
            "planetID": self.planetID,
            "peopleID": self.peopleID,
            "id": self.id
            # do not serialize the password, its a security breach
        }