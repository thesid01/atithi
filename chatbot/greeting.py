# -*- coding: utf-8 -*-
"""This module contains the dialogue states for the 'greeting' domain in
the atithi application
"""

from .root import app


@app.handle(intent='greet')
def greet(request, responder):
    responder.frame["for_confirmation"] = 1
    responder.frame["for_confirmation_message"] = "How do you want to choose your tour spot~Based on activities, type, season or difficulty wise?"
    responder.frame["for_denial"] = 1
    responder.frame["for_denial_message"] = "Dont worry you can do a alot more."
    # responder.reply("Namaskar Atithi🙏"+"~"+"I am your virtual travel agent for your adventure. You can now start and stop journey 😀"+"~"+"Are you ready to start to your journey?")
    responder.reply("Namaskar Atithi🙏"+"~"+"I am your virtual travel agent for your adventure." + "~" + "Here is a list of things I can do for you : 😀\n1. Plan your journey.\n2. Search Flights\n3. Search hotels for you.\n4. Search food and restaurants for you.\n5. Track of your Expenses.\n5. Help you in emergency.")


@app.handle(intent='exit')
def exit(request, responder):
    responder.reply("Alright, See you soon"+"~"+"Let me know when you need any help😀")
