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
        ac = ""
        j = 1
        for i in data[0]["activity"].split(","):
            ac += "\n" +str(j) + ": " + i.title()
            j+=1
        data = image_URL + "~" + trivia + "\n*Suggested Activities:* "+ac
        responder.reply(data)
    except:
        responder.reply(NOT_A_SPOT)


@app.handle(domain='general', intent='get_cityintro')
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

# @app.handle(domain='general',intent='change_pref')
# def change_pref(request,responder):
#     responder.params.allowed_intents = ('general.change_hotel_pref','general.change_food_pref')
#     responder.reply('Sure, which preference do you want to change- hotel or food')

# @app.handle(domain='general',intent='change_hotel_pref',has_entity='hotel')
# def change_hotel_pref(request,responder):
#     responder.params.allowed_intents = ('tourism.hotel_pref')
#     responder.reply("Fine, now please tell us any preferences for hotels i.e Number of rooms ac/non-ac/etc.")
    

# @app.handle(domain='general',intent='change_food_pref',has_entity='food')
# def change_food_pref(request,responder):
#     responder.params.allowed_intents = ('tourism.food_pref')
#     responder.reply("Fine, now please tell us any preferences about your food (veg/non-veg/italian/etc)")

@app.handle(intent = 'confirmation')
def confirmation(request, responder):
    if "for_confirmation" in responder.frame:
        if responder.frame["for_confirmation"]:
            responder.frame["for_confirmation"] = None
            responder.reply(responder.frame["for_confirmation_message"])
        else:
            responder.reply("yahan suggestion dalna hai.(in confirm)")
    else:
        responder.reply("yahan suggestion/faq dalna hai.(in confirm)")

@app.handle(intent = 'denial')
def denial(request, responder):
    if "for_denial" in responder.frame:
        if responder.frame["for_denial"]:
            responder.frame["for_denial"] = None
            responder.reply(responder.frame["for_denial_message"])
        else:
            responder.reply("yahan suggestion dalna hai.(in denial)")
    else:
        responder.reply("yahan suggestion/faq dalna hai.(in denial)")



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
