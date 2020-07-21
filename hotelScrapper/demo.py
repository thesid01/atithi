from hotelScrapper.scrapper import getHotels
from hotelScrapper.bookHotel import bookHotel
import datetime

checkin = datetime.date.today()
checkout = checkin + datetime.timedelta(days=1)
guests = 10
rooms = 4
latitude = 28.4131678
longitude = 77.3455704

list_hotels = getHotels(checkin, checkout, guests, rooms, latitude, longitude)

# for i in list_hotels:
#     print(
#         i, end="\n" * 2,
#     )


for i in list_hotels:
    print(
        bookHotel(i["url"], checkin, checkout, rooms, guests, guests_per_room=3),
        end="\n" * 2,
    )

