from twilio.rest import Client
import time
class remainderHelper:
	def __init__(self, f):
		self.firebase = f
		
	def start(self, data):
		for d in data:
			print(d["time"])
			if(int(round(time.time() * 1000))) > d["time"]:
				self.sendMessage(d)
				self.firebase.removeReminder(d["time"])


	def sendMessage(self, v):
		client = Client()
		#export TWILIO_AUTH_TOKEN=e0e696089a9a6a65774500c37edcb963
		#export TWILIO_ACCOUNT_SID=AC589b234a1d386d213e4434b0f148f1f0
		client.messages.create(media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
								body=v["message"],
								from_="whatsapp:+14155238886",
								to="whatsapp:+"+str(v["to"]))
		print("Sending to", v["to"])
