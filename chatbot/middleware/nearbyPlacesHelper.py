import requests
import json
# from amadeus import Client, ResponseError


#foursqaure
Client_Id = "S0FQJMYT1XFY0AN43OIWEHCFX45EMMINQLDVJLYF3WQOWB3O"
Client_Secret="BB2EUR51DR05UBM4AZBUJF5FJNFRAHUUV4ZTLEJBO0F5FPB1"
auth_key="677995554453587190356x6694"

#here
app_id = 'yYqWuslRYjm32pS7z0QS'
api_key = 'kxoiUmn2N2w8uvlKHdAorQTId375O68sxyhA9Yf3cfY'

def getNearByPlaces(location, count, query):
    location = str(location["Latitude"]) + "," + str(location["Longitude"])
    url = 'https://api.foursquare.com/v2/venues/search'
    params = dict(
    client_id=Client_Id,
    client_secret=Client_Secret,
    v='20180323',
    ll=location,
    query=query,
    limit=count,
    radius=10000
    )
    resp = requests.get(url=url, params=params)
    resp = json.loads(resp.text)
    data = []
    for l in resp["response"]["venues"]:
        temp = dict(
            name = l["name"],
            distance = l["location"]["distance"],
            location = l["location"]["formattedAddress"],
            )
        data.append(temp)
    return data

def getCityName(location):
    location = str(location["Latitude"]) + "," + str(location["Longitude"])
    print("getting location name for ", location)
    url = 'https://geocode.xyz'
    params = dict(
        auth= auth_key,
        locate= location,
        json= 1,
        )
    resp = requests.get(url=url, params=params)
    resp = json.loads(resp.text)
    data = dict()
    try :
        data["city"] = resp["city"]
    except:
        print("city name not found")
    try:
        data["state"]=resp["state"]
    except:
        print("state name not found")

    return data

def transit(ori_location, dest_location):
    url = 'https://transit.router.hereapi.com/v8/routes'
    ori_location = str(ori_location["Latitude"]) + "," + str(ori_location["Longitude"])
    dest_location = str(dest_location["Latitude"]) + "," + str(dest_location["Longitude"])
    params = dict(
        origin=ori_location,
        destination=dest_location,
        apikey=api_key)
    
    resp = requests.get(url=url, params=params)
    resp = json.loads(resp.text)
    
    
if __name__ == "__main__":
    # places = getNearByPlaces({"Latitude":26.8563653,"Longitude":80.9429712},5, "Fruit")
    # print(json.dumps(places, indent=4, sort_keys=True))
    # name = getCityName({"Latitude":22.6001182,"Longitude":88.3425502})
    # print(json.dumps(name, indent=4, sort_keys=True))
    transit({"Latitude":23.1787893,"Longitude":79.7284168}, {"Latitude":26.8486748,"Longitude":80.872473})
