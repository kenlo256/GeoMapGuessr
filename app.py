from flask import Flask, render_template, redirect, url_for
import requests
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

# filter out list of bad location for guessing
badGeocode = ["COUNTY", "COUNTRY", "CITY", "STATE"]
BASE = "http://geomapguessr.me:"


def create_button(abbrev):

    full_country_name = requests.post(BASE + "5001/AbbrevToFullname", data={'abbrev': abbrev})
    # OmerAPI avoid full_country_name to get another 3 random country names
    # also randomised to order that fits in the button boxes

    return render_template('index.html')


resultPutRequest = requests.put(BASE + "5001/Result")

resultGetRequest = requests.get(BASE + "5001/Result")


@app.route("/")
def home():
    return render_template("index.html", content="Testing", result=resultGetRequest)


# GUI button for random function
# python doesn't have do while loops :(
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
        geocode_quality = rand_result['results'][0]['locations'][0]['geocodeQuality']

    abbrev = rand_result['results'][0]['locations'][0]['adminArea1']
    map_url = rand_result['results'][0]['locations'][0]['mapUrl']

    final_url = map_url.replace("225,160", "500,500")
    create_button(abbrev)
    return render_template('index.html', mapurl=final_url)


if __name__ == '__main__':
    app.run()
