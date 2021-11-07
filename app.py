from flask import Flask
import requests
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)
#lol
BASEKEN = "http://119.246.146.149:5000/"

responseken = requests.get(BASEKEN + "/hello")

print(responseken.json())

if __name__ == '__main__':
    app.run()