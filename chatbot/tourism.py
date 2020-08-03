# -*- coding: utf-8 -*-
"""This module contains the dialogue states for the 'tourism' domain in
the atithi application
"""
import os
import json
from .root import app
from chatbot.middleware.firebaseHelper import firebaseHelper
import random
from chatbot.middleware import latest_intent as l_t

firebase = firebaseHelper()

@app.handle(intent='start_tour')
def start_tour(request, responder):
    id = request.params.dynamic_resource['id']
    res = firebase.changeStatus(1,id)
    responder.params.target_dialogue_state = "select_tourism_basis"
    responder.reply("How do you want to choose your tour spot?~Any preference on activities, type, season or difficulty?")
    
@app.handle(intent='select_tourism_basis',has_entity='tour_basis')
def select_tour_basis(request, responder):
    print("in basis")
    print(request.entities)
    id = request.params.dynamic_resource['id']
    res = firebase.changeStatus(1,id)
    basis = request.entities[0]["value"][0]["cname"]
    if basis == 'activity':
        responder.params.target_dialogue_state = "select_activity"
        responder.reply("What type of activities would you like to enjoy on the tour.\nTrekking\nWater Sport\nMountianeering")
    if basis == 'type':
        responder.params.target_dialogue_state = "select_type"
        responder.reply("What type of Adventure would you like to go on.\nNature\nHills\nBeach\nFamily")
    if basis == 'season':
        responder.params.target_dialogue_state = "select_season"
        responder.reply("What type of season would you like to go on.\nSummer\nWinter\nMonsoon\nAutumn")
    if basis == 'difficulty':
        responder.params.target_dialogue_state = "select_difficulty"
        responder.reply("What type of difficulty would you like to enjoy on the tour.\nEasy\nModerate\nDifficult")

@app.handle(intent='select_activity',has_entity='activity')
def select_activity(request, responder):
    activity_type = request.entities[0]["value"][0]["cname"]
    spot_list = _fetch_spot_from_kb("activity",activity_type.lower())
    for i in range(len(spot_list[1])):
        spot_list[1][i] = spot_list[1][i].lower()
    responder.frame["spot_list"] = spot_list[1]
    if len(spot_list[0]) > 1:
        responder.params.target_dialogue_state = "select_destination_from_choice"
        reply = "Here are some good options for " + activity_type +" tourism: "+spot_list[0] + "~Select the spot name to travel.~You can always ask me to 'Tell me about spot name' to know more😀"
    else:
        responder.params.target_dialogue_state = "select_tourism_basis"
        reply = "Sorry..Could not understand.~Please try again😕" + "\nHow do you want to choose your tour spot?~Any preference on activities, type, season or difficulty?"
    responder.reply(reply)


@app.handle(intent='select_type', has_entity='tour_type')
def select_type(request, responder):
    type_type = request.entities[0]["value"][0]["cname"]
    spot_list = _fetch_spot_from_kb("type",type_type.lower())
    for i in range(len(spot_list[1])):
        spot_list[1][i] = spot_list[1][i].lower()
    responder.frame["spot_list"] = spot_list[1]
    if len(spot_list[0]) > 1:
        responder.params.target_dialogue_state = "select_destination_from_choice"
        reply = "Here are some good options for " + type_type +" tourism: "+spot_list[0] + "~Select the spot name to travel.~You can always ask me to 'Tell me about spot name' to know more😀"
    else:
        responder.params.target_dialogue_state = "select_tourism_basis"
        reply = "Sorry..Could not understand.~Please try again😕" + "\nHow do you want to choose your tour spot?~Any preference on activities, type, season or difficulty?"
    responder.reply(reply)


@app.handle(intent='select_season',  has_entity='season')
def select_season(request, responder):
    season_type = request.entities[0]["value"][0]["cname"]
    spot_list = _fetch_spot_from_kb("best_season",season_type.lower())
    for i in range(len(spot_list[1])):
        spot_list[1][i] = spot_list[1][i].lower()
    responder.frame["spot_list"] = spot_list[1]
    if len(spot_list[0]) > 1:
        responder.params.target_dialogue_state = "select_destination_from_choice"
        reply = "Here are some good options for " + season_type +" tourism: "+spot_list[0] + "~Select the spot name to travel.~You can always ask a like 'Tell me about spot name' to know more😀"
    else:
        responder.params.target_dialogue_state = "select_tourism_basis"
        reply = "Sorry..Could not understand.~Please try again😕" + "\nHow do you want to choose your tour spot?~Any preference on activities, type, season or difficulty?"
    responder.reply(reply)

@app.handle(intent='select_difficulty', has_entity='difficulty')
def select_difficulty(request, responder):
    difficulty_type = request.entities[0]["value"][0]["cname"]
    spot_list = _fetch_spot_from_kb("level",difficulty_type.lower())
    for i in range(len(spot_list[1])):
        spot_list[1][i] = spot_list[1][i].lower()
    responder.frame["spot_list"] = spot_list[1]
    if len(spot_list[0]) > 1:
        responder.params.target_dialogue_state = "select_destination_from_choice"
        reply = "Here are some good options for " + difficulty_type +" tourism: "+spot_list[0] + "~Select the spot name to travel.~You can always ask a like 'Tell me about spot name' to know more😀"
    else:
        responder.params.target_dialogue_state = "select_tourism_basis"
        reply = "Sorry..Could not understand.~Please try again😕" + "\nHow do you want to choose your tour spot?~Any preference on activities, type, season or difficulty?"
    responder.reply(reply)

@app.handle(intent = 'select_destination', has_entity='spot_name')
def select_destination_from_choice(request, responder):
    id = request.params.dynamic_resource['id']
    try:
        if request.entities[0]["value"][0]["cname"].lower() in responder.frame["spot_list"]:
            data = request.entities[0]["value"][0]["cname"]

            res = firebase.setDest(data,id)
            lat, long = firebase.getCurrLocation(id)

            if lat and long:
                responder.params.allowed_intents = ('tourism.set_source_loc','tourism.set_source','tourism.resume')
                l_t.setIntent('loc_for_source')
                loc = firebase.getCurrLocationName(id)
                msg = "Your current location is "+loc['city']+" and is set as source.~Please tell us the source location or share the new source location if you want to change it, otherwise resume."
                responder.reply("Your destination has been set to:" + data + "\n\n"+msg+"~👍")

            else:
                
                responder.params.allowed_intents = ('tourism.set_source_loc','tourism.set_source')
                l_t.setIntent('loc_for_source')
                msg = "Please tell us the source location or share your location"
                responder.reply("Your destination has been set to:" + request.entities[0]["text"] + "\n"+msg+"~👍")
                # return

        elif request.entities[0]["value"][0]["cname"]:
            data = request.entities[0]["value"][0]["cname"]

            res = firebase.setDest(data,id)
            lat, long = firebase.getCurrLocation(id)

            if lat and long:
                responder.params.allowed_intents = ('tourism.set_source_loc','tourism.set_source','tourism.resume')
                l_t.setIntent('loc_for_source')
                loc = firebase.getCurrLocationName(id)
                msg = "Your current location is "+loc['city']+" and is set as source.\n\nPlease tell us the source location or share the new source location if you want to change it, otherwise resume."
                responder.reply("The selected adventure spot is not under the chosen class,😕~Continuing.....~Your destination has been set to:" + data + "\n\n"+msg)

            else:
                
                responder.params.allowed_intents = ['tourism.set_source_loc','tourism.set_source']
                l_t.setIntent('loc_for_source')
                msg = "Please tell us the source location or share the location"
                responder.reply("The selected adventure spot is not under the chosen class,😕~Continuing.....\nYour destination has been set to:" + request.entities[0]["text"] + "\n"+msg)

        else:
            responder.reply("Oops!😕...We don't find any such spot in our data.~Try some other spot.")
    except IndexError:
        responder.params.target_dialogue_state = "start_tour"
        responder.reply("Sorry😕~I didn't unnderstand, say 'start' to start planning of tour.")
    except KeyError:
        responder.params.target_dialogue_state = "start_tour"
        responder.reply("Sorry😕~I didn't unnderstand, say start to start planning of tour.")
    return

@app.handle(domain='tourism',intent='resume')
def resume(request,responder):
    l_t.delIntent()
    responder.params.target_dialogue_state = 'food_pref'
    responder.reply("Before we personalize your journey, we would like to ask some preferences😀.\nPlease tell us any preferences about your food (veg/non-veg/italian/etc)")

@app.handle(domain='tourism', intent='set_source_loc')
def set_curr_loc(request,responder):
    l_t.delIntent()
    responder.params.target_dialogue_state = 'food_pref'
    responder.reply("Before we personalize your journey, we would like to ask some preferences😀.\nPlease tell us any preferences about your food (veg/non-veg/italian/etc)")

@app.handle(intent='set_source', has_entity='city_name')
def set_source(request, responder):
    l_t.delIntent()
    data = request.entities[0]["value"][0]["cname"]
    id = request.params.dynamic_resource['id']
    res = firebase.setSource(data,id)
    responder.params.target_dialogue_state = 'food_pref'
    # responder.params.allowed_intents = ['tourism.food_pref']
    responder.reply("Before we personalize your journey, we would like to ask some preferences😀.\nPlease tell us any preferences about your food (veg/non-veg/italian/etc)")

@app.handle(intent='food_pref', has_entity='food')
def food_pref(request, responder):
    id = request.params.dynamic_resource['id']
    data=""
    for item in request.entities:
        data += item['value'][0]["cname"]+" "
    res = firebase.setFoodPref(data,id)
    responder.params.target_dialogue_state = 'hotel_pref'
    # responder.params.allowed_intents = ['tourism.hotel_pref']
    responder.reply("That's great😀!~Now do you have any preferences for hotels i.e Number of rooms ac/non-ac/etc.")

@app.handle(intent='hotel_pref')
def hotel_pref(request,responder):
    id = request.params.dynamic_resource['id']
    data={}
    for item in request.entities:
        data[item["type"]]=item["value"][0]["cname"]

    res = firebase.setHotelPref(data,id)
    responder.reply("Thanks😀, I will take care of your comfort throughout the journey~I will remember these preferences along the journey.~Whenever You are hungry or want to have some rest you are free to ask for my help.~I will help you in searching restaurants and hotels😀")



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


def _fetch_spot_from_kb(filter,type):
    spot = app.question_answerer.get(index='spot_data',size=66)
    spot_list = "\n"
    spot_array = []
    map_spot={}
    print(filter, type)
    j = 1
    for i in range(len(spot)):
        if filter in spot[i]:
            if filter=="activity" or filter=="type" or filter == "difficulty":
                print(spot[i][filter].split(","))
                if type in spot[i][filter].split(","):
                    spot_array.append(spot[i]["spot_name"].lower())
                    map_spot[spot[i]["spot_name"].lower()]=spot[i]["image_URL"]
            else :
                if type in spot[i][filter]:
                    spot_array.append(spot[i]["spot_name"].lower())
                    map_spot[spot[i]["spot_name"].lower()]=spot[i]["image_URL"]

    mn = min(3,len(spot_array))
    new_list = random.sample(spot_array, mn)
    print(new_list)

    for i in new_list:
        spot_list += "~"+map_spot[i]+"~ "+i.title() + "\n"
        j = j+1
    
    return [spot_list,new_list]

def _fetch_all_spot_from_kb():
    spot = app.question_answerer.get(index='spot_data',size=66)
    spot_array = []
    for i in range(len(spot)):
        spot_array.append(spot[i]["spot_name"].lower())
    return [spot_array]