import json
import random

def addSpotType(filename):
    # filename = "../data/spot.json"
    f = open(filename,)
    contents = json.load(f) 
    for cluster in contents["clusters"]:
        for state in cluster["states"]:
            for spot in state["spots"]:
                spot["type"] = random.choice(["nature", "family", "camping"])
    f.close()
    with open(filename, 'w') as json_file:
        json.dump(contents, json_file,  indent = 4,)

def getSpotName(filename):
    f = open(filename,)
    s = set()
    contents = json.load(f) 
    for cluster in contents["clusters"]:
        for state in cluster["states"]:
            for spot in state["spots"]:
                s.add(spot["spot_name"])
    return s

def generateMappingjson(data):
    jj = dict(entities=[])
    for i in data :
        i = i.split(" ")
        t = []
        for ii in range(len(i) + 1): 
            for j in range(ii + 1, len(i) + 1): 
                sub = i[ii:j]
                sub = " ".join(sub)
                t.append(sub)
        i = " ".join(i)
        jj["entities"].append(dict(whitelist=t,cname=i))
    return jj

def convertForElasticSearch(filename) :
    f = open(filename,)
    id = 1
    contents = json.load(f) 
    data = []
    for cluster in contents["clusters"]:
        for state in cluster["states"]:
            for spot in state["spots"]:
                spot["id"] = id
                spot["state_id"] = state["state_id"]
                spot["cluster_id"] = cluster["cluster_id"]
                spot["state_name"]  = state["state_name"]
                spot["location"] = str(spot["location"]["Latitude"]) + "," + str(spot["location"]["Longitude"])
                data.append(spot)
                id += 1
    f.close()
    with open(filename, 'w') as json_file:
        json.dump(data, json_file,  indent = 4,)

if __name__ == "__main__":
    # data = getSpotName("../data/spot.json")
    # data = generateMappingjson(data)
    # print(json.dumps(data,indent=4))
    convertForElasticSearch("../data/spot_data.json")
