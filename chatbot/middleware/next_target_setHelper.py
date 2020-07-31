import json

def setTarget(target):
    filename = "target.json"
    f = open(filename,)
    contents = {
        "target" : target
    }
    f.close()
    with open(filename, 'w') as json_file:
        json.dump(contents, json_file,  indent = 4,)

def getTarget():
    filename = "target.json"
    f = open(filename,)
    data = json.load(f)
    return data["target"]

def delTarget():
    setTarget(None)

if __name__ == "__main__":
    # setTarget("targ")
    getTarget()
    delTarget()