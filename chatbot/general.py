import numpy as np
from .root import app
import json
from .helpers import extract_entities_from_type

NOT_A_CITY="Sorry😕...This city is not in India."+"~"+"Let me help you with this🙂"+"~"+"Some popular cities in India are : Lucknow, Goa, Jodhpur,  etc."+"~"+"Please choose another city."
NOT_A_SPOT="Sorry😕...This spot is not in our list."+"~"+"Let me help you with this🙂"+"~"+"Some popular spots in India are : Tarsar Marsar, Nandi Hills, , Spiti Valley etc."+"~"+"Please choose another spot."

@app.handle(intent = 'get_spotinfo', has_entity='spot_name')
def get_spot_info(request, responder):
    try :
        spot_name = "None"
        if request.entities[0]["type"] == "spot_name":
            spot_name = request.entities[0]["value"][0]["cname"]
        else:
            spot_name = request.entities[1]["value"][0]["cname"]
        data = app.question_answerer.get(index='spot_data', spot_name=spot_name)
        trivia= ""
        try:
            trivia = data[0]["trivia"]
        except KeyError:
            trivia = "Trivia is empty now"
        image_URL = data[0]["image_URL"]
        data = image_URL + "~" + trivia
        responder.reply(data)
    except:
        responder.reply(NOT_A_SPOT)

def get_city(request, responder, entity_type):
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
