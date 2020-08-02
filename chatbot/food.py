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
        responder.params.target_dialogue_state = "set_food_pref"
        responder.reply("Sure, please first tell us the preferences for the (veg/non-veg/italian/etc)")
    else:
        responder.frame["for_confirmation"] = 1
        responder.frame["for_confirmation_message"] = "Sure, please tell me where you are or just share your location so that I can assist you in finding nearby restaurants."
        responder.frame["for_denial"] = 1
        responder.frame["for_denial_message"] = "Ok, please first tell us the preferences for the (veg/non-veg/italian/etc)"
        responder.params.allowed_intents = ('food.set_curr_loc_food','food.search_nearby_food','food.search_food_at_dest')
        l_t.setIntent('loc_for_food')
        responder.reply("Your previous preferences for food was: "+res+"\nWould you like to continue?")


@app.handle(domain='food', intent='search_nearby_food')
def search_nearby_food(request,responder):
    print('f')
    l_t.delIntent()
    id = request.params.dynamic_resource['id']
    res = firebase.getFoodPref(id)
    
    if not res:
        responder.params.target_dialogue_state = "set_food_pref"
        responder.reply("Sure, please first tell us the preferences for the (veg/non-veg/italian/etc)")
    else:
        try:
            lat,long = firebase.getCurrLocation(id)
            if lat and long:
                res_msg = getRestaurant(id, lat, long)
                if res_msg=='':
                    responder.reply("Oops! I cannot find any restaurants near you, must be a remote place 🙂~why don't you try searching with a place name.....")
                else:
                    responder.frame["for_confirmation"] = 1
                    responder.frame["for_confirmation_message"] = "Yay ..I found some restaurants nearby you🌮~Go and enjoy some yummy local food there😋~Below is list of restaurants, check it out:\n"+res_msg
                    responder.frame["for_denial"] = 1
                    responder.frame["for_denial_message"] = "Ok, please first tell us the preferences for the (veg/non-veg/italian/etc)"
                    responder.reply("Your previous preferences for food was: "+res+"\nWould you like to continue?")
        except (TypeError,AttributeError):
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
    res = firebase.getFoodPref(id)
    
    if not res:
        responder.params.target_dialogue_state = "set_food_pref"
        responder.reply("Sure, please first tell us the preferences for the (veg/non-veg/italian/etc)")
    else:
        res_msg = getRestaurant(id,lat,long)
        if res_msg=='':
            responder.reply("Oops! I cannot find any restaurants near you, must be a remote place 🙂~why don't you try searching with a place name.....")
        else:
            responder.frame["for_confirmation"] = 1
            responder.frame["for_confirmation_message"] = "There are some restaurants at your destination😋~"+"Kindly check out the following list:\n~"+res_msg
            responder.frame["for_denial"] = 1
            responder.frame["for_denial_message"] = "Ok, please first tell us the preferences for the (veg/non-veg/italian/etc)"
            responder.reply("Your previous preferences for food was: "+res+"\nWould you like to continue?")

@app.handle(domain='tourism',intent='food_pref', has_entity='food')
def set_food_pref(request, responder):
    id = request.params.dynamic_resource['id']
    data=""
    for item in request.entities:
        data += item['value'][0]["cname"]+" "
    res = firebase.setFoodPref(data,id)
    responder.params.allowed_intents = ('food.set_curr_loc_food','food.search_nearby_food','food.search_food_at_dest')   # responder.params.allowed_intents = ['tourism.hotel_pref']
    responder.reply("I have set the food preferences. You can now search restaurants 😊")

def _fetch_spot_from_kb(spot_name):
    spots = app.question_answerer.get(index='spot_data')
    j = 1
    lat,long = "", ""
    for i in range(len(spots)):
        if spot_name in spots[i]["spot_name"]:
            loc = spots[i]["location"]
            lat,long = loc.split(',')
            break
    return lat,long