def getDate(d):
    data = "{day}%2F{month}%2F{year}".format(
        day=d.strftime("%d"), month=d.strftime("%m"), year=d.strftime("%Y")
    )
    return data


def getConfiguration(rooms, guests, guests_per_room):
    rooms_config = str(rooms)
    total = guests
    for i in range(rooms):
        if total >= guests_per_room:
            rooms_config = "{rooms_config}-{guests_per_room}_0".format(
                rooms_config=rooms_config, guests_per_room=guests_per_room
            )
            total = total - guests_per_room
        else:
            rooms_config = "{rooms_config}-{total}_0".format(
                rooms_config=rooms_config, total=total
            )
    return rooms_config


def extractValue(s):
    s = s[1 : len(s) - 2]
    arr = s.split()
    for i in arr:
        if i[0:7] == "content":
            return i[9:-1]


def prepareEntry(job_elem):
    name = job_elem.find(
        "h3", class_="listingHotelDescription__hotelName d-textEllipsis"
    ).text.strip()

    rating = extractValue(str(job_elem.find(attrs={"itemprop": "ratingValue"})))

    address = job_elem.find(attrs={"itemprop": "streetAddress"}).text.strip()

    distance = job_elem.find(
        "span", class_="listingHotelDescription__distanceText"
    ).text.strip()

    image = extractValue(str(job_elem.find(attrs={"itemprop": "image"})))

    url = extractValue(str(job_elem.find(attrs={"itemprop": "url"})))

    return {
        "name": name,
        "rating": rating,
        "address": address,
        "distance": distance,
        "image": image,
        "url": url,
    }


def getURL(checkin, checkout, guests, rooms, latitude, longitude):
    return "https://www.oyorooms.com/search?location=Around%20me&city=&searchType=locality&coupon=&checkin={checkin}&checkout={checkout}&roomConfig%5B%5D=1&showSearchElements=false&guests={guests}&rooms={rooms}&countryName=India&latitude={latitude}&longitude={longitude}&sort=distance&sortOrder=ascending".format(
        checkin=checkin,
        checkout=checkout,
        guests=guests,
        rooms=rooms,
        latitude=latitude,
        longitude=longitude,
    )
