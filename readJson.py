import json
with open('plants.json', newline='' ,encoding="utf-8") as jsonfile:
    data = json.load(jsonfile)
    # 或者這樣
    # data = json.loads(jsonfile.read())
    for i in data['plants']:
        print(i['name'])
        print(i['temp'])
        print(i['humid'])
        print(i['lightTime'])
            