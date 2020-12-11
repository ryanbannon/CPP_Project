import json

with open('leagueTable.json') as json_file:
    data = json.load(json_file)
    for p in data['records']:
        print(p['team'])