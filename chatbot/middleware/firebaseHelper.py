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
	
	def existID(self, id):
		res = self.db.child("user").get()
		id_list=[]
		for num in res.each():
			id_list.append(num.key())
		if id in id_list:
			return True
		else:
			return False

	def createID(self,data):
		print("Adding user",data)
		res = self.db.child("user").child(data).child("status").set(0)
		return res

	def changeStatus(self, data, id):
		res = self.db.child("user").child(id).child("status").set(data)
		return res

	def setDest(self,data,id):
		res = self.db.child("user").child(id).child("location").child("destinations").set(data)
		return res

	def setSource(self,data,id):
		res = self.db.child("user").child(id).child("location").child("source").set(data)
		return res
		
	def setCurrLocation(self,data, id):
		print("Seting Location",data, "for", id)
    		res = self.db.child("user").child(id).child("location").child("current").set(data)
		return res	
	
 	def getCurrLocation(self, id):
		return self.db.child("user").child(id).child("location").get()
  
	def setRemainder(self, data, id):
		print("setting remainder", data, "for", id)
		results = self.db.child("user").child(id).child("remainder").child(int(round(time.time() * 1000))).set(data)
	
	def getRemainders(self):
		users = self.db.child("user").get()
		remainders = []
		for user in users.val():
			remainders.append({"id":user, "remainders" : self.db.child("user").child(user).child("remainder").get()})
		return remainders
