import logging

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from middleware.firebaseHelper import firebaseHelper
from middleware.remainderHelper import remainderHelper

from mindmeld.components import NaturalLanguageProcessor
from mindmeld.components.dialogue import Conversation
from mindmeld import configure_logs

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import atexit
import time


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

        @self.app.route("/", methods=["POST"])
        def handle_message():  # pylint: disable=unused-variable
            id = request.values.get('From','') #Getting number from which message came
            # print(request.values) #uncomment this to dif deeper
            incoming_msg = request.values.get('Body', '').lower()
            result = self.firebase.addNumber(id)
            location = {
                'Latitude': request.values.get('Latitude',''),
                'Longitude' : request.values.get('Longitude','')
            }
            if request.values.get('Latitude','') and request.values.get('Longitude',''):
                result = self.firebase.setLocation(location, id)
                resp = MessagingResponse()
                msg = resp.message()
                msg.body("We remembered your current location")
                return str(resp)
            else :
                resp = MessagingResponse()
                msg = resp.message()
                params = dict(dynamic_resource =dict(id=id)) #Used to send dynamic id of the user making query
                response_text = self.conv.say(incoming_msg, params=params)[0]
                msg.body(response_text)
                return str(resp)

    def run(self, host="localhost", port=7150):
        self.app.run(host=host, port=port)
    
    def start_remainder(self):
        remainder_service = remainderHelper()
        remainder_service.start(self.firebase.getRemainders())


if __name__ == '__main__':
    app = Flask(__name__)
    configure_logs()
    server = WhatsappBotServer(name='whatsapp', app_path='.')
    
    # create schedule for printing time
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=server.start_remainder,
        trigger=IntervalTrigger(seconds=60*60),
        id='send_remainders',
        name='send remainder every minute',
        replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    
    port_number = 8080
    print('Running server on port {}...'.format(port_number))
    server.run(host='localhost', port=port_number)

