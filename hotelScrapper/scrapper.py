from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from hotelScrapper.utils import getDate, getURL, prepareEntry
from hotelScrapper.bookHotel import bookHotel
import json


def getHotels(checkin, checkout, guests, rooms, latitude, longitude):
    # checkin = getDate(checkin)
    # checkout = getDate(checkout)
    url = getURL(checkin, checkout, guests, rooms, latitude, longitude)
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    webpage = urlopen(req).read()
    page = soup(webpage, "html.parser")
    results = page.find(id="root")
    job_elems = results.find_all("div", class_="hotelCardListing__descriptionWrapper")
    list_hotels = []
    for job_elem in job_elems:
        list_hotels.append(prepareEntry(job_elem))
    return list_hotels

if __name__ == "__main__":

    hotel_list = getHotels("", "", guests=4, rooms=2, latitude="18.708889", longitude="73.476667")
    print(json.dumps(hotel_list, indent=4, sort_keys=True))

