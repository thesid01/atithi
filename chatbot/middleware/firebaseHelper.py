import pyrebase
import time

config = {
  "apiKey": "AIzaSyBiv6ZNCNcoHDiOkAhq9vHKiG0AqE2VjFY",
  "authDomain": "atithi-sih-2020.firebaseapp.com",
  "databaseURL": "https://atithi-sih-2020.firebaseio.com/",
  "storageBucket": "atithi-sih-2020.appspot.com"
}

class firebaseHelper:
	def __init__(self):
		self.config = config
		self.firebase = pyrebase.initialize_app(config)
		self.db = self.firebase.database()

	def addNumber(self,data):
		print("Adding user",data)
		results = self.db.child("user").child(data).child("id").set(data)
		return results

	def setLocation(self,data, id):
		print("Seting Location",data, "for", id)
		results = self.db.child("user").child(id).child("location").set(data)
		return results

	def setRemainder(self, data, id):
		print("setting remainder", data, "for", id)
		results = self.db.child("user").child(id).child("remainder").child(int(round(time.time() * 1000))).set(data)
	
	def getRemainders(self):
		users = self.db.child("user").get()
		remainders = []
		for user in users.val():
			remainders.append({"id":user, "remainders" : self.db.child("user").child(user).child("remainder").get()})
		return remainders