from twilio.rest import Client
class remainderHelper:
	def start(self, data):
		for user in data:
			id = user["id"]
			temp = user["remainders"].val()
			print(temp)
			if temp!=None:
				for k, v in user["remainders"].val().items():
					self.sendMessage(id,v)
	
	def sendMessage(self, id, v):
		client = Client()
		# export TWILIO_AUTH_TOKEN=36418b6fe7615bd068ad13f614bdc19d
		# export TWILIO_ACCOUNT_SID=ACc47f3cc342412b7097ad6f6c6fe19398
		# client.messages.create(body=v["message"],from_="whatsapp:+14155238886", to_=id)
		print("Sending to", id)
		
