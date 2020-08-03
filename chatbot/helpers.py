def extract_entities_from_type(request, entity_type):
    return [e for e in request.entities if e['type'] == entity_type]

def _fetch_general_user_suggestion():
    suggestion = app.question_answerer.get(index='user_suggestions')
    return suggestion[random.randrange(0,len(suggestion))]