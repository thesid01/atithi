from twilio.rest import Client
import time
class remainderHelper:
	def __init__(self, f):
		self.firebase = f
		
	def start(self, data):
		for d in data:
			if(int(round(time.time() * 1000))) > d["time"]:
				self.sendMessage(d)
				self.firebase.removeReminder(d["time"])


	def sendMessage(self, v):
		client = Client()
		# export TWILIO_AUTH_TOKEN=36418b6fe7615bd068ad13f614bdc19d
		# export TWILIO_ACCOUNT_SID=ACc47f3cc342412b7097ad6f6c6fe19398
		client.messages.create(media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
								body=v["message"],
								from_="whatsapp:+14155238886",
								to="whatsapp:+"+str(v["to"]))
		print("Sending to", v["to"])
