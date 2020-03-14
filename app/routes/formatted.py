from flask import jsonify
from flask import current_app as app
from ..data import get_data
from nested_lookup import get_occurrence_of_value
from cachetools import cached, TTLCache


@app.route('/formatted')
@cached(cache=TTLCache(maxsize=1024, ttl=900))
def full():
    # Get all the categories.
    confirmed = get_data('confirmed')
    deaths    = get_data('deaths')
    recovered = get_data('recovered')

    # prepare output dictionary
    output = []

    # Formatting
    for locationConfirmed in confirmed["locations"]:
        deathsData = {}
        recoversData = {}

        # find matching region for deaths & recovered
        targetCoordniates = locationConfirmed["coordinates"]
        
        # search for location match: death
        for locationDeaths in deaths["locations"]:
            # check for matching coordinates
            if locationDeaths["coordinates"] == targetCoordniates:
                deathsData = locationDeaths

        # search for location match: recovered
        for locationRecovers in recovered["locations"]:
            # check for matching coordinates
            if locationRecovers["coordinates"] == targetCoordniates:
                recoversData = locationRecovers

                
        # add the death statistics to the object
        locationOutput = {
            'location': locationConfirmed["country"],
            'coordinates': targetCoordniates,
            'confirmed': locationConfirmed,
            'deaths': deathsData,
            'recovered': recoversData
        }

        # add current location to the output
        output.append(locationOutput)

    return jsonify(output)