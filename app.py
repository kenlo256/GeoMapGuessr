from flask import Flask, render_template, redirect, url_for
import requests
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

# filter out list of bad location for guessing
badGeocode = ["COUNTY", "COUNTRY", "CITY", "STATE"]
BASE = "http://geomapguessr.me:"
mapquest_get_request = requests.get("http://www.mapquestapi.com/geocoding/v1/reverse?"
                                  "key=P6SlkwXEUSNGa2y0MdU45AXA3LADkReB&location="
                                  "-55.671610,-3.914930"
                                  "&includeRoadMetadata=true&includeNearestIntersection=true");

@app.route("/")
def home():
    return render_template("index.html", content="Testing")


# GUI button for random function
# python doesn't have do while loops reeeeeee
@app.route("/rand")
def rand():
    geocode_quality = "COUNTRY"

    while geocode_quality in badGeocode:
        response_omer = requests.get(BASE + "5000/hello")
        rand_coordinate = response_omer.json()

        latitude = rand_coordinate['latitude']
        longitude = rand_coordinate['longitude']

        mapquest_get_request = requests.get("http://www.mapquestapi.com/geocoding/v1/reverse?"
                                  "key=P6SlkwXEUSNGa2y0MdU45AXA3LADkReB&location="
                                  + latitude + "," + longitude +
                                  "&includeRoadMetadata=true&includeNearestIntersection=true");

        rand_result = mapquest_get_request.json()
        geocode_quality = randresult['results'][0]['locations'][0]['geocodeQuality']

    map_url = rand_result['results'][0]['locations'][0]['mapUrl']
    final_url = map_url.replace("225,160", "500,500")
    print(rand_result)

    return render_template('index.html', mapurl=final_url)


def create_button():
    abbrev = mapquest_get_request['result'][0]['locations'][0]['adminArea1']
    abbrev_to_full = requests.post(BASE + "5001/AbbrevToFullname", data={'abbrev': abbrev})


resultPutRequest = requests.put(BASE + "5001/Result")
resultGetRequest = requests.get(BASE + "5001/Result")
# results display on the web
if __name__ == '__main__':
    app.run()
