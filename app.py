from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

#FFFFFFFFFFF
class HelloWorld(Resource):
    def get(self):
        return "Jello"

    def post(self):
        return "Posted:"


api.add_resource(HelloWorld, "/hello")

if __name__ == '__main__':
    app.run()
