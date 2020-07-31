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

@app.handle(domain='reminder', intent='reminder_start')
def reminder_start(request, responder):
    responder.params.target_dialogue_state = 'targ'
    nth.setTarget("targ")
    responder.reply("Yeah Sure! I will set the reminder. Please tell message to send you.")

@app.handle(domain='reminder', intent='reminder_time', has_entity='time')
def get_time(request, responder):
    id = request.params.dynamic_resource['id']
    #try:
    if responder.frame["message"] is None:
        responder.reply("Did not gwt it.")
    else:
        print(request.entities)
        # In request.entities it is showing on digit 
        samay = request.entities[0]["text"]
        print(samay)
        pattern = '%d/%m/%Y %H'
        epoch = int(time.mktime(time.strptime(datetime.datetime.today().strftime("%d/%m/%Y")+" "+samay, pattern)))
        message = responder.frame["message"]
        responder.frame["message"] = None
        firebase.setReminder(data={
            "to": id,
            "time" : epoch,
            "message": message
        })
        responder.reply("I have set a reminder, " +message+" at " + samay)
    #except :
    #    responder.reply("Retry")

@app.handle(targeted_only = True)
def targ(request, responder):
    nth.delTarget()
    message = request.text
    responder.frame["message"] = message
    responder.reply("I will set a reminder for "+message + " At what time?")