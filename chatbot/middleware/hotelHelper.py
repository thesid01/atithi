from hotelScrapper.scrapper import getHotels
from chatbot.middleware.firebaseHelper import firebaseHelper
import json

firebase = firebaseHelper()

def hotelList(id, latitude, longitude):

    r,b,p,a = firebase.getHotelPref(id)
    if r is None :
        return None
    rooms,guests,price = calc_params(r,b,p)
    hotel_list = getHotels('','',guests,rooms,latitude,longitude)
    with open('hotel.json', 'w') as outfile:
        json.dump(hotel_list, outfile, indent=4)
    hotel_msg=''
    for i in range(min(len(hotel_list),5)):
        hotel_obj = hotel_list[i]
        name = hotel_obj['name']
        rating = hotel_obj['rating']
        if not rating:
            rating = 'NA'
        url = hotel_obj['url']
        hotel_msg += ''.join("*Hotel Name*: {name}\n*Rating*: {rating}⭐\n*Link*: {url} ~".format(name=name,rating=rating,url=url))
    return hotel_msg


def calc_params(rooms,beds,price):
    
    if rooms is not '':
        rooms = rooms.split(' ')[0]
        rooms = int(rooms)
        guests = 2*rooms
    else:
        rooms = 1

    if beds is not '':    
        guests = beds.split(' ')[0]
        guests = 2*int(guests)
    else:
        guests = 2

    if price is not '':
        price = price.split(' ')[1]
        price = int(price)
    else:
        price = 5000
    return rooms, guests, price