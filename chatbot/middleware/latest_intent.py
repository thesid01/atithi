import json

def setIntent(intent):
    filename = "latest_intent.json"
    f = open(filename,)
    contents = {
        "intent" : intent
    }
    f.close()
    with open(filename, 'w') as json_file:
        json.dump(contents, json_file,  indent = 4,)

def getIntent():
    filename = "latest_intent.json"
    f = open(filename,)
    data = json.load(f)
    return data["intent"]

def delIntent():
    setIntent(None)

if __name__ == "__main__":
    # setintent("targ")
    getIntent()
    delIntent()
