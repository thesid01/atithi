from utils import getDate, getConfiguration


def bookHotel(url, checkin, checkout, rooms, guests, guests_per_room):

    rooms_config = getConfiguration(rooms, guests, guests_per_room)
    checkin = getDate(checkin)
    checkout = getDate(checkout)
    return "{url}?checkin={checkin}&checkout={checkout}&rooms_config={rooms_config}&guests={guests}&rooms={rooms}&selected_rcid=1&modal=bookingSummary".format(
        url=url,
        checkin=checkin,
        checkout=checkout,
        rooms_config=rooms_config,
        guests=guests,
        rooms=rooms,
    )
