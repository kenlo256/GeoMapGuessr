from flask import Flask, render_template, redirect, url_for
import requests
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

# filter out list of bad location for guessing
badGeocode = ["COUNTY", "COUNTRY", "CITY", "STATE"]
BASE = "http://geomapguessr.me:"

@app.route("/")
def home():
    return render_template("index.html", content="Testing")


# GUI button for random function
# python doesn't have do while loops reeeeeee
@app.route("/rand")
def rand():
    geocodequality = "COUNTRY"
    mapquestgetrequest = requests.get("http://www.mapquestapi.com/geocoding/v1/reverse?"
                                  "key=P6SlkwXEUSNGa2y0MdU45AXA3LADkReB&location="
                                  "-55.671610,-3.914930"
                                  "&includeRoadMetadata=true&includeNearestIntersection=true");

    while geocodequality in badGeocode:
        responseomer = requests.get(BASE + "5000/hello")
        randcoordinate = responseomer.json()

        latitude = randcoordinate['latitude']
        longitude = randcoordinate['longitude']

        mapquestgetrequest = requests.get("http://www.mapquestapi.com/geocoding/v1/reverse?"
                                  "key=P6SlkwXEUSNGa2y0MdU45AXA3LADkReB&location="
                                  + latitude + "," + longitude +
                                  "&includeRoadMetadata=true&includeNearestIntersection=true");

        randresult = mapquestgetrequest.json()
        geocodequality = randresult['results'][0]['locations'][0]['geocodeQuality']

    print(randresult)
    mapurl = randresult['results'][0]['locations'][0]['mapUrl']
    render_template("index.html", mapurl=mapurl)
    return redirect('/')


# display the static map and change size=500,500 by changing the url

# prompt user input from a input box from the web
resultPutRequest = requests.put(BASE + "5001/Result")
resultGetRequest = requests.get(BASE + "5001/Result")
# results display on the web
if __name__ == '__main__':
    app.run()