import random
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


# We kinda made a fatal mistake. We can not have two APIs running on the same URI...

class Coordinates(Resource):
    def get(self):
        latitude = format(random.uniform(-90, 90), '.6f')
        longitude = format(random.uniform(-180, 180), '.6f')
        return {"latitude": latitude, "longitude": longitude}  # AMAZING API!!!! BEST API EVER!!


api.add_resource(Coordinates, "/hello")

if __name__ == '__main__':
    app.run()
