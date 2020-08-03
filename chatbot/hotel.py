"""This module contains the dialogue states for the 'hotel' domain in
the atithi application
"""
#"+"~"+"
import os
import json
from .root import app
from chatbot.middleware.firebaseHelper import firebaseHelper
from chatbot.middleware.hotelHelper import hotelList
import random
from chatbot.middleware import latest_intent as l_t


firebase = firebaseHelper()

@app.handle(intent='start_flow_hotel')
def start_flow_hotel(request, responder):
    id = request.params.dynamic_resource['id']
    _,_,_,res = firebase.getHotelPref(id)
    if res is None:
        responder.params.target_dialogue_state = "set_hotel_pref"
        responder.reply("Sure, please first tell us the preferences for the hotels (number of rooms/ac/non-ac/etc)")
    else:
        r,b,p,a = firebase.getHotelPref(id)
        if a==0:
            a='non ac'
        else:
            a='ac'
        pref = ' '.join([r,b,p,a])
        responder.frame["for_confirmation"] = 1
        responder.frame["for_confirmation_message"] = "Sure😀"+"~"+"Can you tell me destination or city in which you are or just share your location so that I can assist you finding Hotels near you"
        responder.frame["for_denial"] = 1
        responder.frame["for_denial_message"] = "Ok, please first tell us the preferences for the hotels (number of rooms/ac/non-ac/etc)"
        responder.params.allowed_intents = ('hotel.set_curr_loc_hotel','hotel.search_nearby_hotel','hotel.searc_hotel_at_dest','general.present_city')
        l_t.setIntent('loc_for_hotel')
        responder.reply("Your previous preferences for hotel was: "+pref+"\nWould you like to continue")


@app.handle(domain='hotel', intent='search_nearby_hotel')
def search_nearby_hotel(request,responder):
    print('f')
    l_t.delIntent()
    id = request.params.dynamic_resource['id']

    _,_,_,res = firebase.getHotelPref(id)
    if res is None:
        responder.params.target_dialogue_state = "set_hotel_pref"
        responder.reply("Sure, please first tell us the preferences for the hotels (number of rooms/ac/non-ac/etc)")
    
    else:
        try:
            lat,long = firebase.getCurrLocation(id)
            if lat and long:
                hotel_msg = "We are facing issue with our scrapper rght now."
                try:
                    hotel_msg = hotelList(id,lat,long)
                except:
                    responder.reply(hotel_msg)
                if hotel_msg == '':
                    responder.reply("Currently, We don't have any hotels for you😕 But you can always try saying find hotels near " + firebase.getDest(id)+"~"+"I will be there to help you 🙂")
                else:
                    r,b,p,a = firebase.getHotelPref(id)
                    if a==0:
                        a='non ac'
                    else:
                        a='ac'
                    pref = ' '.join([r,b,p,a])
                    responder.frame["for_confirmation"] = 1
                    responder.frame["for_confirmation_message"] = "I have found some hotels🛏 near by you, you can check it out:\n~"+hotel_msg
                    responder.frame["for_denial"] = 1
                    responder.frame["for_denial_message"] = "Ok, please first tell us the preferences for the hotels (number of rooms/ac/non-ac/etc)"
                    responder.reply("Your previous preferences for hotel was: "+pref+"\nWould you like to continue")
            else :
                responder.reply("I Didn't understand😕.\n Try saying find hotels near " + firebase.getDest(id))
        except (TypeError):
            responder.params.target_dialogue_state = "search_at_curr"
            responder.reply("Oops ! Sorry, can you please share your location first so that I can assist you in finding hotels nearby you...🙂")


@app.handle(domain='hotel',intent='set_curr_loc_hotel')
def search_hotel_at_curr(request, responder):
    l_t.delIntent()
    # code for getting nearest_city for the loc
    id = request.params.dynamic_resource['id']
    lat,long = firebase.getCurrLocation(id)
    # end
    _,_,_,res = firebase.getHotelPref(id)
    print(res)
    if res is None:
        responder.params.target_dialogue_state = "set_hotel_pref"
        responder.reply("Sure, please first tell us the preferences for the hotels (number of rooms/ac/non-ac/etc)")
    else:
        try:
            # code for getting hotels list
            hotel_msg = hotelList(id,lat,long)
            if hotel_msg is None:
                responder.reply("We don't have any hotels for you😕. You can always try saying "+ _fetch_find_hotel_in_suggestion()["suggestion"] + firebase.getDest(id))
            else:
                responder.reply("I have found some hotels at your current location."+"~"+"Checkout the following list of hotels:\n~"+hotel_msg+"\n")
        except :
            responder.reply("Ooops!"+"~"+"Sorry..We couldn't find best hotels at your current location😕."+"~"+"Please try sending your location again")


@app.handle(domain='hotel',intent='search_hotel_at_dest', has_entity='spot_name')
def search_hotel_at_dest(request, responder):
    l_t.delIntent()
    id = request.params.dynamic_resource['id']
    _,_,_,res = firebase.getHotelPref(id)
    
    if res is None:
        responder.params.target_dialogue_state = "set_hotel_pref"
        responder.reply("Sure, please first tell us the preferences for the hotels (number of rooms/ac/non-ac/etc)")
    else:
        spot_name = request.entities[0]["value"][0]["cname"]
        lat,long = _fetch_spot_from_kb(spot_name)
        print(lat,long)
        hotel_msg = hotelList(id,lat,long)
        if hotel_msg is None:
            responder.reply("Currently, We don't have any hotel preferences for you😕.\nYou can set your preference saying. ➡" + _fetch_hotel_pref_suggestion()["suggestion"])
        else:
            r,b,p,a = firebase.getHotelPref(id)
            if a==0:
                a='non ac'
            else:
                a='ac'
            pref = ' '.join([r,b,p,a])
            responder.frame["for_confirmation"] = 1
            responder.frame["for_confirmation_message"] = "Yupp"+"~"+"I have found some hotel🏘 at your destination"+"~"+"Check out the following list of hotels:\n~"+hotel_msg
            responder.frame["for_denial"] = 1
            responder.frame["for_denial_message"] = "Ok, please first tell us the preferences for the hotels (number of rooms/ac/non-ac/etc)"
            responder.reply("Your previous preferences for hotel was: "+pref+"\nWould you like to continue")
    
@app.handle(domain='tourism',intent='hotel_pref')
def set_hotel_pref(request, responder):
    id = request.params.dynamic_resource['id']
    data={}
    for item in request.entities:
        data[item["type"]]=item["value"][0]["cname"]

    res = firebase.setHotelPref(data,id)
    responder.params.allowed_intents = ('hotel.set_curr_loc_hotel','hotel.search_nearby_hotel','hotel.searc_hotel_at_dest')

    responder.reply('I have set the hotel preferences. You can now search hotels 😊')

def _fetch_spot_from_kb(spot_name):
    spots = app.question_answerer.get(index='spot_data', size=66)
    lat,long = "", ""
    for i in range(len(spots)):
        if spot_name.lower() == spots[i]["spot_name"].lower():
            loc = spots[i]["location"].lower()
            lat,long = loc.split(',')
            break
    return lat,long

def _fetch_hotel_pref_suggestion():
    suggestion = app.question_answerer.get(index='hotel_pref_suggestion')
    return suggestion[random.randrange(0,len(suggestion))]

def _fetch_find_hotel_in_suggestion():
    suggestion = app.question_answerer.get(index='find_hotel_in_suggestion')
    return suggestion[random.randrange(0,len(suggestion))]
