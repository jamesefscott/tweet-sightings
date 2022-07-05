from app import app
from flask import render_template, request, jsonify, make_response
from .sightings_scraping import get_sightings

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/run-script", methods=["POST"])
def run_script():

    req = request.get_json()
    sightings = get_sightings(req)

    sightings_response = {'sightings': sightings}
    
    res = make_response(jsonify(sightings_response), 200)

    return res