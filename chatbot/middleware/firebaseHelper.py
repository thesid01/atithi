import pyrebase

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
