from chatbot.middleware.firebaseHelper import firebaseHelper
import json
import requests
#firebase = firebaseHelper()
def flightsList(id):
	#source = firebase.getSource(id)
	#dest = firebase.getDest(id)

	#dep_iata = 'NYC'
	#arr_iata =  'BOM'
	#params = {
	#  'access_key': '0daa66a6a2e0ffe46000bcfd8ebb5488',
	#  'dep_iata' : dep_iata,
	#  'arr_iata' : arr_iata
	#}
	#api_result = requests.get('https://api.distancematrix.ai/maps/api/distancematrix/json?origins=Lucknow&destinations=Kanpur&key=c0OoJyZxEWOKf1icLZU58i9WEdgcp')
	#api_result.json()
	#print(api_result.json())
	list_flights = ""
	flight_dummy = [["12546", "Rs. 4785", "9:35 am", "6:30 pm", "https://www.nomadicmatt.com/travel-tips/how-to-find-a-cheap-flight/"], ["87495", "Rs. 4785", "12:35 am", "9:30 am", "https://theblondeabroad.com/top-tips-for-finding-cheap-flights/"], ["56552", "Rs. 12,800", "5:35 pm", "10:00 pm", "https://www.cheapflights.com/news/"], ["2556", "Rs. 5555", "7:11 am", "1:30 pm", "https://www.farecompare.com/blog/"]]
	for _ in flight_dummy:
		list_flights += ''.join("*Flight No*: {no}\n*Price*: {price}\n*Arrival Time*:{a_time}\n*Departure Time*: {time}\n*Book Here*:{url}~").format(no=_[0], price=_[1], time=_[2], a_time=_[3], url=_[4])

	return list_flights
