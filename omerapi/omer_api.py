import random
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///countries.db'

db = SQLAlchemy(app)
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('name', type=str, required=True, help='You have to enter the name of a country')

countryfield = {'name': fields.String}


class Countries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)


class Coordinates(Resource):
    def get(self):
        latitude = format(random.uniform(-90, 90), '.6f')
        longitude = format(random.uniform(-180, 180), '.6f')
        return {"latitude": latitude, "longitude": longitude}


class RandCountries(Resource):
    @marshal_with(countryfield)
    def get(self):
        args = parser.parse_args()
        result = db.session.execute('SELECT * FROM Countries ORDER BY RANDOM() LIMIT 4').fetchall()
        for x in range(len(result) - 1):
            if result[x][1] == args['name']:
                result[x], result[3] = result[3], result[x]
                break
        result.pop()
        return result


api.add_resource(Coordinates, "/hello")
api.add_resource(RandCountries, "/countriesrand")

if __name__ == '__main__':
    app.run()
