from flask import Flask, render_template, request, redirect
import requests
import random
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

# filter out list of bad location for guessing
badGeocode = ["COUNTY", "COUNTRY", "CITY", "STATE"]
BASE = "http://geomapguessr.me:"
correct_country = ""

def create_button(abbrev):
    global correct_country
    full_country_name = (requests.post(BASE + "5001/AbbrevToFullname", data={'abbrev': abbrev})).json()
    other_countries = (requests.get(BASE + "5000/countriesrand", data={'name': full_country_name})).json()
    correct_country = full_country_name
    list_of_countries = []
    print(correct_country)
    for x in other_countries:
        list_of_countries.append(x['name'])
    list_of_countries.append(full_country_name)
    random.shuffle(list_of_countries)

    return list_of_countries


@app.route("/")
def home():
    result_get_request = requests.get(BASE + "5001/result")
    return render_template("index.html", content="Testing", result=result_get_request)


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
    countries_array = create_button(abbrev)

    return render_template('index.html', mapurl=final_url, button1=countries_array[0], button2=countries_array[1],
                           button3=countries_array[2], button4=countries_array[3])


@app.route("/checkbutton", methods=["POST"])
def checkbutton():
    if request.form['button'] == correct_country:
        requests.put(BASE + "5001/result", data={'country': correct_country})
    else:
        redirect("/rand")
    result_get_request = requests.get(BASE + "5001/result")

    return render_template('index.html', result=result_get_request.json())


if __name__ == '__main__':
    app.run()
