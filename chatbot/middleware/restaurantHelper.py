import requests
import json

API_KEY = "c4a9f379abbb27fe1d84b22779654870"
headers = {
	"Accept": "application/json",
	"user-key": "c4a9f379abbb27fe1d84b22779654870"	
}

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
	
def getRestaurant(location, count):
	url = 'https://developers.zomato.com/api/v2.1/geocode?lat='+str(location["Latitude"])+'&lon='+str(location["Longitude"])
	r = requests.get(url, headers=headers)
	r = json.loads(r.content)
	restaurants = []
	for res in r["nearby_restaurants"]:
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
		if len(restaurants) >= count:
			break
	data = {
		"topCuisine":r["popularity"]["top_cuisines"],
		"nearby_restaurants" : restaurants,
	}
	return data

def getRestaurantsbyCuisine(location, cuisine):
	pass

if __name__ == "__main__":
	hotels = getHotels({"Latitude":26,"Longitude":80},5)
	print(json.dumps(hotels, indent=4, sort_keys=True))
	print(json.dumps(getRestaurantDetails(2300780), indent=4, sort_keys=True))
