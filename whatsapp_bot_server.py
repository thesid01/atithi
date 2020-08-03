import logging
import json
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from chatbot.middleware.firebaseHelper import firebaseHelper
from chatbot.middleware.remainderHelper import remainderHelper

from mindmeld.components import NaturalLanguageProcessor
from mindmeld.components.dialogue import Conversation
from mindmeld import configure_logs

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from twilio.rest import Client

import atexit
import time
import validators
from chatbot.middleware import latest_intent as l_t
from chatbot.middleware import next_target_setHelper as nth


#TWILIO_ACCOUNT_SID = 'ACc47f3cc342412b7097ad6f6c6fe19398'
#TWILIO_AUTH_TOKEN = '36418b6fe7615bd068ad13f614bdc19d'
#export TWILIO_AUTH_TOKEN=e0e696089a9a6a65774500c37edcb963
#export TWILIO_ACCOUNT_SID=AC589b234a1d386d213e4434b0f148f1f0
#client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
client = Client()
class WhatsappBotServer:

    def __init__(self, name, app_path, nlp=None):
        """
        Args:
            name (str): The name of the server.
            app_path (str): The path of the MindMeld application.
            nlp (NaturalLanguageProcessor): MindMeld NLP component, will try to load from app path
              if None.
        """
        self.firebase = firebaseHelper()
        self.app = Flask(name)
        if not nlp:
            self.nlp = NaturalLanguageProcessor(app_path)
            self.nlp.load()
        else:
            self.nlp = nlp
        self.conv = Conversation(nlp=self.nlp, app_path=app_path)
        self.logger = logging.getLogger(__name__)
        self.url = None

        @self.app.route("/", methods=["POST"])
        def handle_message():  # pylint: disable=unused-variable
            # print(request.values)
            # Getting number from which message came
            id = request.values.get('From', '')
            id = id.split('+')[1]
            # print(request.values) #uncomment this to dif deeper
            exist = self.firebase.existID(id)
            if not exist:
                result = self.firebase.createID(id)

            incoming_msg = request.values.get('Body', '').lower()
            location = {
                'Latitude': request.values.get('Latitude', ''),
                'Longitude': request.values.get('Longitude', '')
            }
            if request.values.get('Latitude', '') and request.values.get('Longitude', ''):
                intent = l_t.getIntent()
                print(intent)
                result = self.firebase.setCurrLocation(location, id)
                resp = MessagingResponse()
                msg = resp.message()
                params = dict(dynamic_resource=dict(id=id))
                if intent == 'loc_for_source':
                    incoming_msg = "source for location"
                elif intent == 'loc_for_hotel':
                    incoming_msg = "location for hotel"
                elif intent == 'loc_for_food':
                    incoming_msg = "location for food"
                else:
                    incoming_msg = "general location"
                try:
                    response_text = self.conv.say(incoming_msg, params=params)[0]
                    messages = response_text.split("~")
                    for msg in messages:
                        if msg:
                            sendMessage(msg, id)
                except IndexError:
                    msg.body("Didn't understand. sorry")
                
            else:
                resp = MessagingResponse()
                msg = resp.message()
                # Used to send dynamic id of the user making query
                params = None
                if nth.getTarget() == None :
                    params = dict(dynamic_resource =dict(id=id)) #Used to send dynamic id of the user making query
                else:
                    params = dict(dynamic_resource =dict(id=id),target_dialogue_state=nth.getTarget())
                try:
                    response_text = self.conv.say(incoming_msg, params=params)[0]
                    messages = response_text.split("~")
                    for msg in messages:
                        if msg:
                            sendMessage(msg, id)
                except IndexError:
                    msg.body("Didn't understand. sorry")
            return str(resp)

        def sendMessage(msg, number):
            # Change the from whatsapp number with your twilio account number
            valid=validators.url(msg)
            if valid :
                self.url = msg
            else:
                if self.url:
                    client.messages.create(body=msg, from_="whatsapp:+14155238886", to="whatsapp:+"+str(number), media_url=[self.url])
                    self.url = None
                else:
                    client.messages.create(body=msg, from_="whatsapp:+14155238886", to="whatsapp:+"+str(number))

    def run(self, host="localhost", port=7150):
        self.app.run(host=host, port=port)

    def start_remainder(self):
        remainder_service = remainderHelper(self.firebase)
        remainder_service.start(self.firebase.getReminders())


if __name__ == '__main__':
    app = Flask(__name__)
    configure_logs()
    server = WhatsappBotServer(name='whatsapp', app_path='./chatbot')
    nth.delTarget()
    l_t.delIntent()
    # create schedule for printing time
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=server.start_remainder,
        trigger=IntervalTrigger(seconds=5*60),
        id='send_remainders',
        name='send remainder every minute',
        replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    port_number = 8080
    print('Running server on port {}...'.format(port_number))
    server.run(host='localhost', port=port_number)
