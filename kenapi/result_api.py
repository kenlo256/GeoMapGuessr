from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///result.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    counter = db.Column(db.Integer)


class CountrySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Country

    id = ma.auto_field()
    name = ma.auto_field()
    counter = ma.auto_field()


db.create_all()

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('country', type=str, required=True, help='country name required')


class Result(Resource):
    def put(self):
        args = parser.parse_args()
        q = db.session.query(Country).filter_by(name=args['country'])
        if q.exists():
            q.counter += 1
        else:
            result = Country(name=args['country'], counter=1)
        db.session.add(result)
        db.session.commit()
        country = CountrySchema()
        return country.dump(result), 201
#tryout


api.add_resource(Result, "/result")


if __name__ == '__main__':
    app.run()
