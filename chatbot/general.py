import numpy as np
from .root import app
import json
from .helpers import extract_entities_from_type

NOT_A_CITY="Sorry😕...This city is not in India."+"~"+"Let me help you with this🙂"+"~"+"Some popular cities in India are : Lucknow, Goa, Jodhpur,  etc."+"~"+"Please choose another city."
@app.handle(domain='general', intent='getcity_intro')
def get_city(request, responder):
    name = request.frame.get('city_name')

    # if the user has provided a new name, replace the existing name with it
    try:
        name_ent = extract_entities_from_type(request, 'city_name')
        name = name_ent[0]['value'][0]['cname']
    except IndexError:
        if not name:
            return responder

    # If name in database, fetch details from knowledge base
    if name:
        responder = _fetch_from_kb(responder, name, entity_type)
    return responder

@app.handle(domain='general',intent='change_pref')
def change_hotel_pref(request,responder):
    responder.params.allowed_intents = ('general.change_hotel_pref','general.change_food_pref')
    responder.reply('Sure, which preference do you want to change- hotel or food')

@app.handle(domain='general',intent='change_hotel_pref')
def change_hotel_pref(request,responder):
    responder.params.allowed_intents = ('tourism.hotel_pref')
    responder.reply("Fine, now please tell us any preferences for hotels i.e Number of rooms ac/non-ac/etc.")
    

@app.handle(domain='general',intent='change_food_pref')
def change_hotel_pref(request,responder):
    responder.params.allowed_intents = ('tourism.food_pref')
    responder.reply("Fine, now please tell us any preferences about your food (veg/non-veg/italian/etc)")

def _fetch_from_kb(responder, name, entity_type):
    """
    This function is used the fetch a particular information about the given employee
    from the knowledge base.
    """

    city = app.question_answerer.get(index='city_data', city_name=name)
    entity_option = city[0][entity_type]

    responder.slots['city_name'] = name
    responder.slots[entity_type] = entity_option
    return responder
