from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///result.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    counter = db.Column(db.Integer)


db.create_all()


class CountrySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Country

    id = ma.auto_field()
    name = ma.auto_field()
    counter = ma.auto_field()


parser1 = reqparse.RequestParser(bundle_errors=True)
parser2 = reqparse.RequestParser(bundle_errors=True)
parser1.add_argument('country', type=str, required=True, help='country name required')
parser2.add_argument('abbrev', type=str, required=True, help='abbreviation required')

countriesDB = json.loads(open('kenapi/data/en/countries.json').read())


class Result(Resource):
    def put(self):
        args = parser1.parse_args()
        if db.session.query(db.exists().where(Country.name == args['country'])).scalar():
            db.session.query(Country)\
                    .filter(Country.name == args['country']).\
                    update({"counter": (Country.counter + 1)})
        else:
            result = Country(name=args['country'], counter=1)
            db.session.add(result)
        db.session.commit()
        return 201

    def get(self):
        records = Country.query.all()
        country_schema = CountrySchema()
        return [country_schema.dump(record) for record in records]

    def delete(self):
        db.session.query(Country).delete()
        return 201


class AbbrevToFullname(Resource):
    def post(self):
        args = parser2.parse_args()
        for country in countriesDB:
            if args['abbrev'].lower() == country['alpha2']:
                return country['name']
        return 204


api.add_resource(Result, "/result")
api.add_resource(AbbrevToFullname, "/AbbrevToFullname")
if __name__ == '__main__':
    db.create_all()
    app.run()
