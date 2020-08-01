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
                if spot["spot_name"] != "spot1":
                    print(spot["spot_name"])
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

def convertForElasticSearch(file, filename) :
    f = open(file,)
    id = 1
    contents = json.load(f) 
    data = []
    for cluster in contents["clusters"]:
        for state in cluster["states"]:
            for spot in state["spots"]:
                temp = dict()
                temp["id"] = str(id)
                temp["state_id"] = str(state["state_id"])
                temp["cluster_id"] = str(cluster["cluster_id"])
                temp["state_name"]  = state["state_name"]
                for k in spot:
                    temp[k] = spot[k]
                temp["location"] = str(spot["location"]["Latitude"]) + "," + str(spot["location"]["Longitude"])
                temp['spot_id'] = str(spot["spot_id"])
                temp["level"] = random.choice(["Easy","Moderate","Difficult"])
                if "best_season" in spot:
                    temp["best_season"] = spot["best_season"][0]
                if spot["spot_name"] != "spot1" and spot["spot_name"] != "":
                    data.append(temp)
                    id += 1
    f.close()
    with open(filename, 'w') as json_file:
        json.dump(data, json_file,  indent = 4,)

if __name__ == "__main__":
    convertForElasticSearch("../data/spot.json", "../data/spot_data.json")
