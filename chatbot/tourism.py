# -*- coding: utf-8 -*-
"""This module contains the dialogue states for the 'tourism' domain in
the atithi application
"""
import os
import json
from .root import app
from chatbot.middleware.firebaseHelper import firebaseHelper

firebase = firebaseHelper()

@app.handle(intent='start_tour')
def start_tour(request, responder):
    id = request.params.dynamic_resource['id']
    res = firebase.changeStatus(1,id)
    responder.params.target_dialogue_state = "select_tourism"
    responder.reply("What type of Adventure would you like to go on.\n1. Nature\n2. Camping\n3. Family")
    

@app.handle(intent='select_tourism')
def select_tourism(request, responder):
    tourism_type = request.entities[0]["text"]
    spot_list = _fetch_spot_from_kb(tourism_type.lower())
    for i in range(len(spot_list[1])):
        spot_list[1][i] = spot_list[1][i].lower()
    responder.frame["spot_list"] = spot_list[1]
    if len(spot_list[0]) > 1:
        responder.params.target_dialogue_state = "select_destination_from_choice"
        reply = "Here are some good options for " + tourism_type +" tourism: "+spot_list[0] + "Select the spot name to travel.\nYou can always ask a like 'Tell me about spot name'"
    else:
        responder.params.target_dialogue_state = "select_tourism"
        reply = "Could not understand try again" + "\nWhat type of Adventure would you like to go on.\n1. Nature\n2. Camping\n3. Family"
    responder.reply(reply)


@app.handle(intent = 'select_destination', has_entity='spot_name')
def select_destination_from_choice(request, responder):

    try:
        if request.entities[0]["text"] in responder.frame["spot_list"]:
            id = request.params.dynamic_resource['id']
            data = request.entities[0]["text"]

            res = firebase.setDest(data,id)
            #######################
            #Extract location name
            #based on current coord
            ######################
            responder.params.target_dialogue_state = "set_source"
            responder.reply("Your destination has been set to:" + request.entities[0]["text"] + "\nYour current location is: dummy and is set as source" +
            "\nPlease tell us the source loaction if you want to change it'")

        else:
            all_cities = _fetch_all_spot_from_kb()
            if request.entities[0]["text"] in all_cities[0]:
                responder.params.target_dialogue_state = "set_source"
                responder.reply("You have choosen city not from recommenend list.\nContinuing.....")
    except IndexError:
        responder.params.target_dialogue_state = "start_tour"
        responder.reply("Wrong Choice");
    return


@app.handle(intent='set_source', has_entity='city_name')
def set_source(request, responder):
    data = request.entities[0]["text"]
    id = request.params.dynamic_resource['id']
    res = firebase.setSource(data,id)
    responder.params.target_dialogue_state = 'food_pref'
    # responder.params.allowed_intents = ['tourism.food_pref']
    responder.reply("Before we personalize your journey, we would like to ask some preferences.\nPlease tell us any preferences about your food (veg/italian/etc)")

@app.handle(intent='food_pref', has_entity='food')
def food_pref(request, responder):
    id = request.params.dynamic_resource['id']
    data=""
    for item in request.entities:
        data += item['value'][0]["cname"]+" "
    print(data)
    res = firebase.setFoodPref(data,id)
    responder.params.target_dialogue_state = 'hotel_pref'
    # responder.params.allowed_intents = ['tourism.hotel_pref']
    responder.reply('Good, Now have you any preferences for hotels(number of rooms/ac/non-ac/etc)')

@app.handle(intent='hotel_pref')
def hotel_pref(request,responder):
    id = request.params.dynamic_resource['id']
    data={}
    for item in request.entities:
        print(item)
        data[item["type"]]=item["value"][0]["cname"]

    print(data)
    res = firebase.setHotelPref(data,id)
    responder.reply('Thank you we will remember these preferences along the journey.\nYou are free to search restaurants and hotels anytime you feel according to your location')



def _fetch_city_from_kb(tourism_type):
    city = app.question_answerer.get(index='city_data')
    city_list = "\n"
    city_array = []
    j = 1
    for i in range(len(city)):
        if tourism_type in city[i]["tourism_type"]:
            city_list += str(j)+": "+city[i]["city_name"] + "\n"
            j = j+1
            city_array.append(city[i]["city_name"])
    return [city_list,city_array]


def _fetch_spot_from_kb(tourism_type):
    spot = app.question_answerer.get(index='spot_data')
    spot_list = "\n"
    spot_array = []
    j = 1
    for i in range(len(spot)):
        if tourism_type in spot[i]["type"]:
            spot_list += str(j)+": "+spot[i]["spot_name"] + "\n"
            j = j+1
            spot_array.append(spot[i]["spot_name"])
    return [spot_list,spot_array]

def _fetch_all_spot_from_kb():
    spot = app.question_answerer.get(index='spot_data')
    spot_array = []
    for i in range(len(spot)):
        spot_array.append(spot[i]["spot_name"])
    return [spot_array]