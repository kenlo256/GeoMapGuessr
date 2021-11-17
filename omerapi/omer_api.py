import random
from flask import Flask
from flask_restful import Api, Resource, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
# configures the location & type of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///countries.db'
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('name', type=str, required=True, help='You have to enter the name of a country')

db = SQLAlchemy(app)

# this is the format that the output is marshalled with
countryfield = {'name': fields.String}


# defines a table in the database that stores countries
class Countries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)

# A Resource that has a GET method which returns a random coordinate
# The coordinates obey the formatting of the external API for easy extraction
class Coordinates(Resource):
    def get(self):
        latitude = format(random.uniform(-90, 90), '.6f')
        longitude = format(random.uniform(-180, 180), '.6f')
        return {"latitude": latitude, "longitude": longitude}


# A Resource that has a GET method which pulls 4 random countries from the database
# It compares the country in the URL with the first 3 countries
# If there is a match, the matching country is swapped with the fourth country
# The fourth country is discarded and it returns 3 countries in the requests.Response Object format
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


# Adds the resources to the API
api.add_resource(Coordinates, "/hello")
api.add_resource(RandCountries, "/countriesrand")

if __name__ == '__main__':
    app.run()
