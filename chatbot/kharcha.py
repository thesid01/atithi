"""This module contains the dialogue states for the 'hotel' domain in
the atithi application
"""
import time
import os
import json
from .root import app
from chatbot.middleware.firebaseHelper import firebaseHelper
from chatbot.middleware.hotelHelper import hotelList
from mindmeld.components.dialogue import DialogueFlow as df
import random
import datetime
from chatbot.middleware import next_target_setHelper as nth

firebase = firebaseHelper()

@app.handle(domain='kharcha', intent='spent')
def spent(request, responder):
    id = request.params.dynamic_resource['id']
    first, second, nxt = "", "" , ""
    if 'value' in request.entities[0]['value'][0] :
        first = request.entities[0]["value"][0]["value"]
        nxt = 1
    else:
        first = request.entities[1]["value"][0]["value"]
        nxt = 0
    second = request.entities[nxt]['value'][0]['cname']
    print(first, second)
    firebase.setExpenditure(first,id)
    responder.reply("I have noted it down.")

@app.handle(domain='kharcha', intent='view_expenditure')
def view_expenditure(request, responder):
    id = request.params.dynamic_resource['id']
    total = firebase.getTotalExpenditure(id)
    message = "Your total expenditure 💶 : *" + str(total[0]) +"*\n"
    if total[1] != "":
        message += "Your daily expenses are:\n" + total[1]
    responder.reply(message)
