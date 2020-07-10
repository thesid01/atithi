import numpy as np
from .root import app
import json
from .helpers import extract_entities_from_type

NOT_A_CITY="City not found in India"

@app.handle(intent='get_cityintro', has_entity='city_intro')
def get_info_age(request, responder):
    responder = get_city(request, responder, 'city_intro')
    try:
        responder.reply("About {city_name}: {city_intro}")
    except KeyError:
        responder.reply(NOT_A_CITY)
    return

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

@app.handle(intent='select_user_location')
def select_user_location(request, responder):
    file = open('userInfo.json','r')
    data = json.loads(file.read())
    file.close()
    try:
        datastore = {
            "to" : data["from"],
            "from": request.entities[0]["text"]
            }
    except IndexError:
        datastore = {
            "to" : "",
            "from" : ""
        }
    file = open('userInfo.json','w')
    json.dump(datastore, file)
    file.close()
    responder.reply("Your current location is set")
