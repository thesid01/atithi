"""This module contains the dialogue states for the 'flights' domain in
the atithi application
This file will send message related to flight data
"""

import os
from .root import app
from chatbot.middleware.firebaseHelper import firebaseHelper
from chatbot.middleware.flights_data import flightsList
import json
import requests

firebase = firebaseHelper()

@app.handle(intent='start_flow')
def start_flow(request, responder):
    # responder.params.target_dialogue_state = "hotel.set_current_loc"
    responder.params.allowed_intents = ['general.set_current_loc','hotel.search_nearby','hotel.search_at_dest']
    responder.reply("Sure, please tell us the the destination name or just share your location if you want to search flights")

@app.handle(domain='flight', intent='show_flights')
def show_flight_data(request,responder):
    
    id = request.params.dynamic_resource['id']

    try:
        source = firebase.getCurrLocationName(id)
        dest = firebase.getDest(id)
        if source and dest:
            flight_msg = flightsList(id)
            print(flight_msg)
            responder.reply("Here is the list of flights you can take 🛫\n ~"+flight_msg)
    except (TypeError):
        responder.reply("Sorry I didn't find any Flights😕")
