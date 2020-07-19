"""This module contains the dialogue states for the 'hotel' domain in
the atithi application
"""

import os
import json
from .root import app
from chatbot.middleware.firebaseHelper import firebaseHelper

firebase = firebaseHelper()

@app.handle(intent='start_flow')
def start_flow(request, responder):
    responder.params.target_dialogue_state = "select_location"
    responder.reply("Sure, please tell us the the destination name")

@app.handle(domain='hotel',intent='select_location')
def select_loaction(request, responder):
    id = request.params.dynamic_resource['id']
    s = request.entities[0]["text"]
    s = s.split(' ')
    print(s)
    dest = firebase.getDest(id)
    dest = dest.split(' ')
    loc=''
    print(dest)
    for i in s:
        for j in dest:
            if i==j:
                loc=i
                break
    
    print(loc)

    # code for getting nearest_city for the loc


    # end

    # code for getting hotels list


    # end

    responder.params.target_dialogue_state = "select_hotel"
    responder.reply("list of hotels")

@app.handle(targeted_only=True)
def select_hotel(request, responder):
    print('hotel select karega')
    responder.reply('fantastic you can book it from this url')

