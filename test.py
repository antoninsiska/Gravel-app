

import json

with open("data.json", "r") as file:
    data = json.load(file)

rides = {
        "Red": "demo.py",
        "Green": "None",
        "Black": "None",
        "Pink": "None",
        "Purple": "None",
        "Yellow": "None",
        "Blue": "None"

    }
def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct
dataPretty = data['data'][0]['rides']
print(type(dataPretty[0]))
print(type(rides))

