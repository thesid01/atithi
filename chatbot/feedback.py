
import os
import json
from .root import app
from chatbot.middleware.firebaseHelper import firebaseHelper

firebase = firebaseHelper()
@app.handle(domain='feedback', has_entity='feedback')
def confirm_feedback(request, responder):
    id = request.params.dynamic_resource['id']
    firebase.setFeedback(id, responder.frame["message"])
    responder.reply("Thank you for your feedback🙂~")

