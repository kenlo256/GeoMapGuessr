import random
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///countries.db'

db = SQLAlchemy(app)

class Countries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(57), nullable=False)

class Coordinates(Resource):
    def get(self):
        latitude = format(random.uniform(-90, 90), '.6f')
        longitude = format(random.uniform(-180, 180), '.6f')
        return {"latitude": latitude, "longitude": longitude}  # AMAZING API!!!! BEST API EVER!!

    def put(self):
        db.session.add(Countries(name="egrrth"))
        db.session.commit()
        return ''


db.create_all()
api.add_resource(Coordinates, "/hello")

if __name__ == '__main__':
    app.run()
