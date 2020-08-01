"""This module contains the dialogue states for the 'food' domain in
the atithi application
"""

import os
import json
from .root import app
from chatbot.middleware.firebaseHelper import firebaseHelper
from chatbot.middleware.restaurantHelper import getRestaurant
from chatbot.middleware import latest_intent as l_t

firebase = firebaseHelper()

@app.handle(intent='start_flow_food')
def start_flow_food(request, responder):
    id = request.params.dynamic_resource['id']
    res = firebase.getFoodPref(id)
    if not res:
        responder.params.allowed_intents = ('tourism.food_pref')
        responder.reply("Sure, please first tell us the preferences for the (veg/non-veg/italian/etc)")
    else:
        responder.params.allowed_intents = ('food.set_curr_loc_food','food.search_nearby_food','food.search_food_at_dest')
        l_t.setIntent('loc_for_food')
        responder.reply("Sure, please tell me where you are or just share your location so that I can assist you in finding nearby restaurants.")


@app.handle(domain='food', intent='search_nearby_food')
def search_nearby_food(request,responder):
    print('f')
    l_t.delIntent()
    id = request.params.dynamic_resource['id']
    res = firebase.getFoodPref(id)
    
    if not res:
        responder.params.allowed_intents = ('tourism.food_pref')
        responder.reply("Sure, please first tell us the preferences for the (veg/non-veg/italian/etc)")
    else:
        try:
            lat,long = firebase.getCurrLocation(id)
            if lat and long:
                res_msg = getRestaurant(id, lat, long)
                print('d')
                responder.reply("Yay ..I found some restaurants nearby you🌮~Go and enjoy some yummy local food there😋~Below is list of restaurants, check it out:\n"+res_msg)
        except (TypeError,AttributeError):
            print('g')
            responder.params.target_dialogue_state = "search_food_at_curr"
            responder.reply('I know you are hungry😅.~But can you please share your location first so that I can help you in finding restaurants nearby you...🙂')


@app.handle(domain='food',intent='set_curr_loc_food')
def search_food_at_curr(request, responder):
    l_t.delIntent()

    # code for getting nearest_city for the loc
    id = request.params.dynamic_resource['id']
    lat,long = firebase.getCurrLocation(id)
    # end

    res_msg = getRestaurant(id,lat,long)
    responder.reply("Yummy food is waiting for you😋!~I found some restaurants at your current location:\nHere is the list of restaurants you can check it out:\n\n"+res_msg)

@app.handle(domain='food',intent='search_food_at_dest', has_entity='spot_name')
def search_at_dest(request, responder):
    l_t.delIntent()

    spot_name = request.entities[0]["value"][0]["cname"]
    id = request.params.dynamic_resource['id']
    lat,long = _fetch_spot_from_kb(spot_name)
    res = firebase.getFoodPref('id')
    
    if not res:
        responder.params.allowed_intents = ('tourism.food_pref')
        responder.reply("Sure, Can you tell me your food preference😋?~So What would you like to have like veg, non-veg, italian or something else?")
    else:
        res_msg = getRestaurant(id,lat,long)

        responder.reply("There are some restaurants at your destination😋~"+"Kindly check out the following list:\n~"+res_msg)

def _fetch_spot_from_kb(spot_name):
    spots = app.question_answerer.get(index='spot_data')
    j = 1
    for i in range(len(spots)):
        if spot_name in spots[i]["spot_name"]:
            loc = spots[i]["location"]
            lat,long = loc.split(',')
            break
    return lat,long