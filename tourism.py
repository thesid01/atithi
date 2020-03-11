# -*- coding: utf-8 -*-
"""This module contains the dialogue states for the 'tourism' domain in
the atithi application
"""

from .root import app

@app.handle(intent='tourism_type')
def tourism(request, responder):
    tourism_type = request.entities[0]["text"]
    city_list = _fetch_city_from_kb()
    reply = "Here are some good options for " + tourism_type +" tourism: "+city_list + "You can always ask a like \"Tell me about city\""
    responder.reply(reply)


def _fetch_city_from_kb():
    """
    This function is used the fetch cites from the knowledge base.
    """
    city = app.question_answerer.get(index='city_data')
    city_list = "\n"
    for i in range(len(city)):
        city_list += str(i+1)+": "+city[i]["city_name"] + "\n"
    return city_list
