import numpy as np
from .root import app
import json
from .helpers import extract_entities_from_type

NOT_A_CITY="Sorry😕...This city is not in India."+"~"+"Let me help you with this🙂"+"~"+"Some popular cities in India are : Lucknow, Goa, Jodhpur,  etc."+"~"+"Please choose another city."
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
