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
    responder.reply("Yeah Sure!😀~I will set the reminder.~First tell me what to remind you?")

@app.handle(domain='reminder', intent='reminder_time')
def get_time(request, responder):
    id = request.params.dynamic_resource['id']
    try:
        if responder.frame["message"] is None:
            responder.reply("Did not get it..😕.~Try Again")
        else:
            # In request.entities it is showing on digit 
            samay = request.entities[0]["value"][0]["value"]
            print(samay)
            pattern = "%Y-%m-%dT%H:%M:%S.%fZ"
            samay = "-".join(samay.split("-")[:-1]) +"Z"
            samay = datetime.datetime.strptime(samay,pattern)
            epoch = datetime.datetime.utcfromtimestamp(0)
            samay = (samay - epoch).total_seconds() * 1000.0
            message = responder.frame["message"]
            responder.frame["message"] = None
            firebase.setReminder(data={
                "to": id,
                "time" : samay,
                "message": "You asked me to remind you for " +message
            })
            responder.reply("I have set a reminder, " +message+" at " +request.text)
    except :
        if "retry_reminder" in responder.frame:
            c = responder.frame["retry_reminder"]
            responder.frame["retry_reminder"] = c + 1
            if(c<3) :
                responder.params.allowed_intents = ['reminder.reminder_time']
                responder.reply("This is not time I think.🤔~Please enter valid time") 
            else:      
                responder.reply("Sorry could not set😕")
        else:
            responder.params.allowed_intents = ['reminder.reminder_time']
            responder.frame["retry_reminder"] = 1
            responder.reply("This is not time I think.🤔~Please enter valid time") 

@app.handle(targeted_only = True)
def targ(request, responder):
    nth.delTarget()
    message = request.text
    responder.frame["message"] = message
    responder.params.allowed_intents = ['reminder.reminder_time']
    responder.reply("I will set a reminder for "+message + ".~At what time?")