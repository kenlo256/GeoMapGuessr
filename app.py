from flask import Flask
import requests

app = Flask(__name__)

BASEKEN = "http://127.0.0.1:5000/"

responseken = requests.get(BASEKEN + "/hello")

print(responseken.json())

if __name__ == '__main__':
    app.run()