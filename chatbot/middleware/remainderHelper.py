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
		# export TWILIO_AUTH_TOKEN=36418b6fe7615bd068ad13f614bdc19d
		# export TWILIO_ACCOUNT_SID=ACc47f3cc342412b7097ad6f6c6fe19398
		client.messages.create(media_url=['https://image.shutterstock.com/image-vector/reminder-red-square-sticker-isolated-260nw-274255889.jpg'],
								body=v["message"],
								from_="whatsapp:+14155238886",
								to="whatsapp:+"+str(v["to"]))
		print("Sending to", v["to"])
