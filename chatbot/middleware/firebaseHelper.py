import pyrebase
import time
from . import nearbyPlacesHelper

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
		if not res.val():
			return False
		else:
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

	def getDest(self,id):
		res = self.db.child("user").child(id).child("location").child("destinations").get().val()
		return res

	def setSource(self,data,id):
		res = self.db.child("user").child(id).child("location").child("source").set(data)
		return res

	def setCurrLocation(self,data, id):
		print("setting Location",data, "for", id)
		res = self.db.child("user").child(id).child("location").child("current").set(data)
		self.setCurrLocationName(data, id)
		return res
		
	def getCurrLocation(self,id):
		lat = self.db.child("user").child(id).child("location").child("current").child("Latitude").get()
		long = self.db.child("user").child(id).child("location").child("current").child("Longitude").get()
		return (lat.val(), long.val())

	def setCurrLocationName(self,data, id):
		print("setting Location Name",data, "for", id)
		res = self.db.child("user").child(id).child("location").child("current").child("location_name").set(nearbyPlacesHelper.getCityName(data))
		return res
	
	def getCurrLocationName(self, id):
		print("getting Location Name", "for", id)
		try:
			res = self.db.child("user").child(id).child("location").child("current").child("location_name").get().val()
			city = res['city']
		except TypeError:
			print('d')
			lat,long = self.getCurrLocation(id)
			coord = {'Latitude': lat, 'Longitude': long}
			self.setCurrLocationName(coord,id)
			res = self.db.child("user").child(id).child("location").child("current").child("location_name").get().val()

		return res

	def setFoodPref(self,data,id):
		print("setting food pref",data, "for", id)
		res = self.db.child("user").child(id).child("preferences").child("food").set(data)
		return res

	def getFoodPref(self,id):
		res = self.db.child("user").child(id).child("preferences").child("food").get()
		return res

	def setHotelPref(self,data,id):
		print("setting hotel pref",data, "for", id)
		res = None
		if 'nof_room' in data.keys():
			res = self.db.child("user").child(id).child("preferences").child("hotel").child("room").set(data['nof_room'])
		if 'nof_bed' in data.keys():
			res = self.db.child("user").child(id).child("preferences").child("hotel").child("bed").set(data['nof_bed'])
		if 'price' in data.keys():
			res = self.db.child("user").child(id).child("preferences").child("hotel").child("price").set(data['price'])
		if 'ac' in data.keys():
			res = self.db.child("user").child(id).child("preferences").child("hotel").child("ac").set(1)
		if 'non-ac' in data.keys():
			res = self.db.child("user").child(id).child("preferences").child("hotel").child("ac").set(0)
		return res

	def getHotelPref(self,id):
		pref = self.db.child("user").child(id).child("preferences").child("hotel").get()
		pref = pref.val()
		if pref is None:
			return None, None, None, None
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

	def setReminder(self, data):
		print("setting remainder", data,)
		return self.db.child("reminder").child(int(round(time.time() * 1000))).set(data)
	
	def removeReminder(self, data):
		print("removing remainder", data)
		self.db.child("reminder").child(data).remove()
	
	def getReminders(self):
		reminders = self.db.child("reminder").get()
		data = []
		if reminders.val() is None :
			return []
		for rem in reminders.val():
			data.append(self.db.child("reminder").child(rem).get().val())
		return data

if __name__ == "__main__":
	f = firebaseHelper()
	f.setReminder({
		"to":"918604074906",
		"time" : int(round(time.time() * 1000)),
		"message": "Hi Siddharth Its time to sleep"
	})
	f.getReminders()