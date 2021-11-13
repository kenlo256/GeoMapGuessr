from flask import Flask
import requests
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)
# filter out list of bad location for guessing
badGeocode = ["COUNTY", "COUNTRY", "CITY", "STATE"]
BASE = "http://geomapguessr.me:"

# GUI button for random function

# python doesn't have do while loops reeeeeee
geocodeQuality = "COUNTRY"
mapQuestGetRequest = requests.get("http://www.mapquestapi.com/geocoding/v1/reverse?"
                                  "key=P6SlkwXEUSNGa2y0MdU45AXA3LADkReB&location="
                                  "-55.671610,-3.914930"
                                  "&includeRoadMetadata=true&includeNearestIntersection=true");

while geocodeQuality in badGeocode:
    responseOmer = requests.get(BASE + "5000/hello")
    randCoordinate = responseOmer.json()

    latitude = randCoordinate['latitude']
    longitude = randCoordinate['longitude']

    mapQuestGetRequest = requests.get("http://www.mapquestapi.com/geocoding/v1/reverse?"
                                  "key=P6SlkwXEUSNGa2y0MdU45AXA3LADkReB&location="
                                  + latitude + "," + longitude +
                                  "&includeRoadMetadata=true&includeNearestIntersection=true");

    randResult = mapQuestGetRequest.json()
    geocodeQuality = randResult['results'][0]['locations'][0]['geocodeQuality']

print(mapQuestGetRequest.json())

# display the static map and change size=450,450 by changing the url

# prompt user input from a input box from the web
resultPutRequest = requests.put(BASE + "5001/Result")
resultGetRequest = requests.get(BASE + "5001/Result")

if __name__ == '__main__':
    app.run()