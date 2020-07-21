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
		print("setting Location",data, "for", id)
		res = self.db.child("user").child(id).child("location").child("current").set(data)
		return res
	def getCurrLocation(self,id):
		lat = self.db.child("user").child(id).child("location").child("current").child("Latitude").get()
		long = self.db.child("user").child(id).child("location").child("current").child("Longitude").get()

		return (lat.val(), long.val())

	def setFoodPref(self,data,id):
		print("setting food pref",data, "for", id)
		res = self.db.child("user").child(id).child("preferences").child("food").set(data)
		return res

	def getFoodPref(self,id):
		res = self.db.child("user").child(id).child("preferences").child("food").get()
		return res

	def setHotelPref(self,data,id):
		print("setting hotel pref",data, "for", id)
		if 'nof_room' in data.keys():
			res = self.db.child("user").child(id).child("preferences").child("hotel").child("room").set(data['nof_room'])
		if 'nof_bed' in data.keys():
			res = self.db.child("user").child(id).child("preferences").child("hotel").child("bed").set(data['nof_bed'])
		if 'price' in data.keys():
			res = self.db.child("user").child(id).child("preferences").child("hotel").child("price").set(data['price'])
		if 'ac' in data.keys():
			res = self.db.child("user").child(id).child("preferences").child("hotel").child("ac").set(1)
		if 'n0n-ac' in data.keys():
			res = self.db.child("user").child(id).child("preferences").child("hotel").child("ac").set(0)
		return res

	def getHotelPref(self,id):
		pref = self.db.child("user").child(id).child("preferences").child("hotel").get()
		pref = pref.val()
		rooms=beds=price=''
		ac=0

		if 'room' in pref.keys():
			rooms = pref["room"]
		if 'bed' in pref.keys():
			beds = pref["bed"]
		if 'price' in pref.keys():
			price = pref["price"]
		if 'ac' in pref.keys():
			ac = pref["ac"]
		return rooms, beds, price, ac

	def setRemainder(self, data, id):
		print("setting remainder", data, "for", id)
		results = self.db.child("user").child(id).child("remainder").child(int(round(time.time() * 1000))).set(data)
	
	def getRemainders(self):
		users = self.db.child("user").get()
		remainders = []
		for user in users.val():
			remainders.append({"id":user, "remainders" : self.db.child("user").child(user).child("remainder").get()})
		return remainders
