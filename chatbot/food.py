"""This module contains the dialogue states for the 'food' domain in
the atithi application
"""

import os
import json
from .root import app
from chatbot.middleware.firebaseHelper import firebaseHelper
from chatbot.middleware.restaurantHelper import getRestaurant

firebase = firebaseHelper()

@app.handle(intent='start_flow_food')
def start_flow_food(request, responder):
    # responder.params.target_dialogue_state = "hotel.set_current_loc"
    responder.params.allowed_intents = ['general.set_current_loc','food.search_nearby_food','food.search_food_at_dest']
    responder.reply("Sure, please tell us the the destination name or just share your location if you want to search restaurants nearby you")

@app.handle(domain='food', intent='search_nearby_food')
def search_nearby_food(request,responder):
    print('f')
    id = request.params.dynamic_resource['id']

    try:
        lat,long = firebase.getCurrLocation(id)
        if lat and long:
            # hotel_msg = hotelList(id,lat,long)
            # print(hotel_msg)
            print('d')
            responder.reply("here is the list of restaurants nearby you:")
    except (TypeError,AttributeError):
        print('g')
        responder.params.target_dialogue_state = "search_food_at_curr"
        responder.reply('Please share your location')


@app.handle(domain='general',intent='set_current_loc')
def search_food_at_curr(request, responder):

    # code for getting nearest_city for the loc
    id = request.params.dynamic_resource['id']
    lat,long = firebase.getCurrLocation(id)
    # end

    # code for getting hotels list
    # hotel_msg = hotelList(id,lat,long)
    # print(hotel_msg)
    responder.reply("here is the list of restaurants at your current location:")


@app.handle(domain='hotel',intent='search_food_at_dest', has_entity='spot_name')
def search_at_dest(request, responder):
    spot_name = request.entities[0]["value"][0]["cname"]
    print(spot_name)
    id = request.params.dynamic_resource['id']
    lat,long = _fetch_spot_from_kb(spot_name)
    print(lat,long)
    # hotel_msg = hotelList(id,lat,long)
    # print(hotel_msg)
    responder.reply("here is the list of restaurants at your destination\n")
    