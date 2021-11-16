from flask import Flask, render_template, request, redirect
import requests
import random
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

# badGeocode contains bad location for guessing for filtering
badGeocode = ["COUNTY", "COUNTRY", "CITY", "STATE"]
# BASE is the DDNS address points to my own hosted server
BASE = "http://geomapguessr.me:"
correct_country = ""


# after the we get the randomised location it trigger the create button location to show all the choices for countries
# total no. box is 4
def create_button(abbrev):
    global correct_country
    # get the correct country name
    full_country_name = (requests.post(BASE + "5001/AbbrevToFullname", data={'abbrev': abbrev})).json()
    # get the random countries name to fill out the box choices
    other_countries = (requests.get(BASE + "5000/countriesrand", data={'name': full_country_name})).json()
    # assign for later correct_country for checking with the right answer
    correct_country = full_country_name
    # turn arrays of randomised country with the right country and convert them to a array of string
    list_of_countries = []
    for x in other_countries:
        list_of_countries.append(x['name'])
    list_of_countries.append(full_country_name)
    # shuffle the order so the player won't can really guess the answer
    random.shuffle(list_of_countries)

    return list_of_countries


@app.route("/")
def home():
    # render page with the result on the database
    result_get_request = requests.get(BASE + "5001/result")
    return render_template("index.html", content="Testing", result=result_get_request.json())


@app.route("/reset")
def reset():
    # delete all the countries so the other player can clear previous history and rerender the page
    requests.delete(BASE + "5001/result")
    result_get_request = requests.get(BASE + "5001/result")
    return render_template("index.html", content="Testing", result=result_get_request.json())


@app.route("/rand")
def rand():
    # initialize with bad location
    geocode_quality = "COUNTRY"
    # this loop generate randomised location until it satisfied the condition of a good guessing location
    # by avoiding bad geocode in geocode_quality, geocodeQuality is described in the external API page
    while geocode_quality in badGeocode:
        # send a get request to Omer's web service for getting the coordinate
        response_omer = requests.get(BASE + "5000/hello")
        rand_coordinate = response_omer.json()

        latitude = rand_coordinate['latitude']
        longitude = rand_coordinate['longitude']
        # call external api to get the information of the randomised coordinate
        mapquest_get_request = requests.get("http://www.mapquestapi.com/geocoding/v1/reverse?"
                                            "key=P6SlkwXEUSNGa2y0MdU45AXA3LADkReB&location="
                                            + latitude + "," + longitude +
                                            "&includeRoadMetadata=true&includeNearestIntersection=true");

        rand_result = mapquest_get_request.json()
        geocode_quality = rand_result['results'][0]['locations'][0]['geocodeQuality']
    # External API MapQuest will output the country adminArea1 in abbreviation form iso 3166 alpha-2
    abbrev = rand_result['results'][0]['locations'][0]['adminArea1']
    # External API gives out map_url to be display on the web
    map_url = rand_result['results'][0]['locations'][0]['mapUrl']
    # replace it with the resolution 500x 500 for more guessable size with more info
    final_url = map_url.replace("225,160", "500,500")
    # after that we call create button, it will output the randomised order array for list of countries
    countries_array = create_button(abbrev)

    return render_template('index.html', mapurl=final_url, button1=countries_array[0], button2=countries_array[1],
                           button3=countries_array[2], button4=countries_array[3])


@app.route("/checkbutton", methods=["POST"])
def checkbutton():
    # since html post doesn't return spaces and strips character after it, so we compare it with substring
    if request.form['button'] == correct_country or request.form['button'] in correct_country:
        requests.put(BASE + "5001/result", data={'country': correct_country})
    else:
        redirect("/rand")
    result_get_request = requests.get(BASE + "5001/result")

    return render_template('index.html', result=result_get_request.json())


if __name__ == '__main__':
    app.run()
