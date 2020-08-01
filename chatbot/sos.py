# -*- coding: utf-8 -*-
from twilio.rest import Client

from .root import app

@app.handle(domain='sos', intent='police_emergency')
def police_emergency(request, responder):
    responder.reply("I think you need police help~Here is the the contact number.~Call📞: +917475758383~Don't worry! I hope your query will be resolved🙂")
    #makecall()
    responder.listen()

@app.handle(domain='sos', intent='medical_emergency')
def medical_emergency(request, responder):
    responder.reply("I think you need medical help.~Call📞: +91755889549~Don't worry! I hope your query will be resolved🙂")
    #makecall()
    responder.listen()

@app.handle(domain='sos', intent='default_emergency')
def default_emergency(request, responder):
    responder.reply("Here is Tourist helpline number.~Call📞: +1800 6785 8696~I hope your query will be resolved.🙂")
    #makecall()
    responder.listen()

#def makecall():
    #client = Client()
    #call = client.calls.create(
                        #url='http://demo.twilio.com/docs/voice.xml',
                        #to='+918887141688',
                        #from_='+917348361073'
                    #)