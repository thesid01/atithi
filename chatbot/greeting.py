# -*- coding: utf-8 -*-
"""This module contains the dialogue states for the 'greeting' domain in
the atithi application
"""

from .root import app


@app.handle(intent='greet')
def greet(request, responder):
    responder.reply("Namaskar Atithi🙏")
    responder.reply("I am your virtual travel agent for your adventure. You can now start and stop journey😀")
    responder.reply("Are you ready to start to your journey ?")
    


@app.handle(intent='exit')
def exit(request, responder):
    responder.reply('Alright, See you soon')
    responder.reply('Byyee')
    responder.reply('Take Care 😀')
