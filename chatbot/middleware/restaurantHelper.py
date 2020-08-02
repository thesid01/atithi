import requests
import json
from chatbot.middleware.firebaseHelper import firebaseHelper


API_KEY = "c4a9f379abbb27fe1d84b22779654870"
headers = {
	"Accept": "application/json",
	"user-key": "c4a9f379abbb27fe1d84b22779654870"	
}

firebase = firebaseHelper()

def getRestaurantDetails(id):
	url = 'https://developers.zomato.com/api/v2.1/restaurant?res_id='+str(id)
	res = requests.get(url, headers=headers)
	res = json.loads(res.content)
	temp = {
		"id" : res["R"]["res_id"],
		"name": res["name"],
		"url" : res["url"],
		"timings": res["timings"],
		"thumb" : res["thumb"],
		"cuisines" : res["cuisines"],
		"average_cost_for_two" : res["currency"] + str(res["average_cost_for_two"]),
		"user_rating" : res["user_rating"]["aggregate_rating"],
		"photos_url" : res["photos_url"],
		"phone_numbers" : res["phone_numbers"]
	}
	return temp
	
def getRestaurant(id,lat,long,count=5):

	food_pref = firebase.getFoodPref(id)
	food_pref = food_pref.split(' ')
	if 'indian' in food_pref:
		food_pref.remove('indian')
	if 'veg' in food_pref:
		food_pref.remove('veg')

	cuisines = '%2C'.join(food_pref)
	cuisines = cuisines+'%2Cnorth%20indian'
	# print(cuisines)
	
	url = 'https://developers.zomato.com/api/v2.1/search?count='+str(count)+'&lat='+str(lat)+'&lon='+str(long)+'&cuisines='+cuisines
	
	# print(url)
	r = requests.get(url, headers=headers)
	r = json.loads(r.content)
	# print(r)
	restaurants = []
	for res in r["restaurants"]:
		res = res["restaurant"]
		temp = {
			"id" : res["R"]["res_id"],
			"name": res["name"],
			"url" : res["url"],
			"thumb" : res["thumb"],
			"cuisines" : res["cuisines"],
			"average_cost_for_two" : res["currency"] + str(res["average_cost_for_two"]),
			"user_rating" : res["user_rating"]["aggregate_rating"],
		}
		restaurants.append(temp)
	res_msg=''
	for i in range(min(len(restaurants),5)):
		res_obj = restaurants[i]
		name = res_obj['name']
		rating = res_obj['user_rating']
		if not rating:
			rating = 'NA'
		url = res_obj['url']
		res_msg += ''.join("*Name*: {name}\n*Rating*: {rating}⭐\n*Link*: {url} ~".format(name=name,rating=rating,url=url))
	return res_msg




if __name__ == "__main__":
	hotels = getRestaurant('917980985665',{"Latitude":22.598885,"Longitude":88.337981},5)
	print(json.dumps(hotels, indent=4, sort_keys=True))
	# print(json.dumps(getRestaurantDetails(2300780), indent=4, sort_keys=True))
