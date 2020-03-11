# -*- coding: utf-8 -*-
"""This module contains the dialogue states for the 'greeting' domain in
the atithi application
"""

from .root import app


@app.handle(intent='greet')
def greet(request, responder):
    responder.reply("Namaskar Atithi, What kind of tour would you like to go on today?")


@app.handle(intent='exit')
def exit(request, responder):
    responder.reply('Alright, See you soon')

@app.handle(default=True)
def default(request, responder):
    responder.reply('Sorry I dont understand try again')
