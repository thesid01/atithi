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
    city_list = _fetch_city_from_kb(tourism_type.lower())
    for i in range(len(city_list[1])):
        city_list[1][i] = city_list[1][i].lower()
    responder.frame["city_list"] = city_list[1]
    if len(city_list[0]) > 1:
        responder.params.target_dialogue_state = "select_destination_from_choice"
        reply = "Here are some good options for " + tourism_type +" tourism: "+city_list[0] + " Type \"select city_name\" to start your journey. \nYou can always ask a like \"Tell me about city\""
    else:
        reply = "Could not understand try again" + "\nWhat type of Adventure would you like to go on.\n1.Nature\n2. Camping\n3. Family"
    responder.reply(reply)


@app.handle(intent = 'select_destination', has_entity='city_name')
def select_destination_from_choice(request, responder):

    try:
        if request.entities[0]["text"] in responder.frame["city_list"]:
            id = request.params.dynamic_resource['id']
            data = request.entities[0]["text"]

            res = firebase.setDest(data,id)
            #######################
            #Extract location name
            #based on current coord
            ######################
            responder.params.target_dialogue_state = "set_source"
            responder.reply("Your destination has been set to:" + request.entities[0]["text"] + "\nYour current location is: dummy and is set as source" +
            "\nIf you want to change the source type 'set your_source_location'")

        else:
            all_cities = _fetch_all_city_from_kb()
            if request.entities[0]["text"] in all_cities:
                responder.reply("You have choosen city not from recommenend list.\n Would you like to continue")
    except IndexError:
        responder.reply("Wrong Choice");
    return


@app.handle(intent='set_source', has_entity='city_name')
def set_source(request, responder):
    data = request.entities[0]["text"]
    id = request.params.dynamic_resource['id']
    res = firebase.setSource(data,id)

    responder.reply("Your source location is set")

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




def recommend_travel_plan(_from, _to,responder):
    if _from == "":
        responder.params.target_dialogue_state = "select_user_location"
        reply = "Awesome could you please tell Your Location so that i can recomment travel plan as I am unaware of where you are?"
    else:
        file = open('userInfo.json','r')
        data = json.loads(file.read())
        file.close()
        try:
            datastore = {
                "to" : _to,
                "from" : data["from"]
            }
        except IndexError:
            datastore = {
                "to" : _to,
                "from" : ""
            }
        file = open('userInfo.json','w')
        json.dump(datastore, file)
        file.close()
        reply = "suggesting flights from "+_from+" to "+_to
    responder.reply(reply)