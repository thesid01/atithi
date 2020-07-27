"""This module contains the dialogue states for the 'hotel' domain in
the atithi application
"""

import os
import json
from .root import app
from chatbot.middleware.firebaseHelper import firebaseHelper
from chatbot.middleware.hotelHelper import hotelList
import random

firebase = firebaseHelper()

@app.handle(intent='start_flow_hotel')
def start_flow_hotel(request, responder):
    # responder.params.target_dialogue_state = "hotel.set_current_loc"
    responder.params.allowed_intents = ['general.set_current_loc','hotel.search_nearby_hotel','hotel.searc_hotel_at_dest']
    responder.reply("Sure, please tell us the the destination name or just share your location if you want to search hotels nearby you")

@app.handle(domain='hotel', intent='search_nearby_hotel')
def search_nearby_hotel(request,responder):
    print('f')
    id = request.params.dynamic_resource['id']

    try:
        lat,long = firebase.getCurrLocation(id)
        if lat and long:
            hotel_msg = hotelList(id,lat,long)
            if hotel_msg is None:
                responder.reply("We don't have any preferences for you. You can always try saying find hotels near " + firebase.getDest(id))
            else:
                responder.reply("I have found some hotels🛏 near by you, you can check it out:\n"+hotel_msg)
        else :
            responder.reply("I Didn't understand😕.\n Try saying find hotels near " + firebase.getDest(id))
    except (TypeError):
        responder.params.target_dialogue_state = "search_at_curr"
        responder.reply('Please share your location')


@app.handle(domain='general',intent='set_current_loc')
def search_hotel_at_curr(request, responder):

    # code for getting nearest_city for the loc
    id = request.params.dynamic_resource['id']
    lat,long = firebase.getCurrLocation(id)
    # end
    try:
        # code for getting hotels list
        hotel_msg = hotelList(id,lat,long)
        if hotel_msg is None:
            responder.reply("We dont have any preferences for you. You can always try saying "+ _fetch_find_hotel_in_suggestion()["suggestion"] + firebase.getDest(id))
        else:
            responder.reply("here is the list of hotels at your current location:\n"+hotel_msg + "\n" + _fetch_find_hotel_in_suggestion()["suggestion"] + firebase.getDest(id))
    except :
        responder.reply("Ooops! Sorry..We couldn't find best hotels at your current location😕, Please try sending your location again")


@app.handle(domain='hotel',intent='search_hotel_at_dest', has_entity='spot_name')
def search_hotel_at_dest(request, responder):
    spot_name = request.entities[0]["value"][0]["cname"]
    print(spot_name)
    print("sidd")
    id = request.params.dynamic_resource['id']
    lat,long = _fetch_spot_from_kb(spot_name)
    print(lat,long)
    hotel_msg = hotelList(id,lat,long)
    if hotel_msg is None:
        responder.reply("Currently, We dont have any hotel preferences for you.\nYou can set your preference saying. ➡" + _fetch_hotel_pref_suggestion()["suggestion"])
    else:
        responder.reply("Yeahh... I have found some hotel🏘 at your destination :\n"+hotel_msg)
        responder.reply("Don't worry ! I will take care of your comfort during the journey.😀")
    print(hotel_msg)
    


def _fetch_spot_from_kb(spot_name):
    spots = app.question_answerer.get(index='spot_data')
    j = 1
    for i in range(len(spots)):
        if spot_name in spots[i]["spot_name"]:
            loc = spots[i]["location"]
            lat,long = loc.split(',')
    return lat,long

def _fetch_hotel_pref_suggestion():
    suggestion = app.question_answerer.get(index='hotel_pref_suggestion')
    return suggestion[random.randrange(0,len(suggestion))]

def _fetch_find_hotel_in_suggestion():
    suggestion = app.question_answerer.get(index='find_hotel_in_suggestion')
    return suggestion[random.randrange(0,len(suggestion))]
