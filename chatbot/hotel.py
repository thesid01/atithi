"""This module contains the dialogue states for the 'hotel' domain in
the atithi application
"""

import os
import json
from .root import app
from chatbot.middleware.firebaseHelper import firebaseHelper
from chatbot.middleware.hotelHelper import hotelList

firebase = firebaseHelper()

@app.handle(intent='start_flow')
def start_flow(request, responder):
    # responder.params.target_dialogue_state = "hotel.set_current_loc"
    responder.params.allowed_intents = ['general.set_current_loc','hotel.search_nearby','hotel.search_at_dest']
    responder.reply("Sure, please tell us the the destination name or just share your location if you want to search hotels nearby you")

@app.handle(domain='hotel', intent='search_nearby')
def search_nearby(request,responder):
    print('f')
    id = request.params.dynamic_resource['id']

    try:
        lat,long = firebase.getCurrLocation(id)
        if lat and long:
            hotel_msg = hotelList(id,lat,long)
            print(hotel_msg)
            responder.reply("here is the list of hotels nearby you:\n"+hotel_msg)
    except (TypeError):
        responder.params.target_dialogue_state = "search_at_curr"
        responder.reply('Please share your location')


@app.handle(domain='general',intent='set_current_loc')
def search_at_curr(request, responder):

    # code for getting nearest_city for the loc
    id = request.params.dynamic_resource['id']
    lat,long = firebase.getCurrLocation(id)
    # end

    # code for getting hotels list
    hotel_msg = hotelList(id,lat,long)
    print(hotel_msg)
    responder.reply("here is the list of hotels at your current location:\n"+hotel_msg)


@app.handle(domain='hotel',intent='search_at_dest', has_entity='spot_name')
def search_at_dest(request, responder):
    spot_name = request.entities[0]["value"][0]["cname"]
    print(spot_name)
    id = request.params.dynamic_resource['id']
    lat,long = _fetch_spot_from_kb(spot_name)
    print(lat,long)
    hotel_msg = hotelList(id,lat,long)
    print(hotel_msg)
    responder.reply("here is the list of hotels at your destination\n"+hotel_msg)
    


def _fetch_spot_from_kb(spot_name):
    spots = app.question_answerer.get(index='spot_data')
    j = 1
    for i in range(len(spots)):
        if spot_name in spots[i]["spot_name"]:
            loc = spots[i]["location"]
            lat,long = loc.split(',')
    return lat,long
