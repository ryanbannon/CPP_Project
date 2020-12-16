import http.client

open("leagueTable.json", 'w').close()

conn = http.client.HTTPSConnection("heisenbug-premier-league-live-scores-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "",
    'x-rapidapi-host': "heisenbug-premier-league-live-scores-v1.p.rapidapi.com"
    }

conn.request("GET", "/api/premierleague/table", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

f = open("leagueTable.json", "a")
f.write(data.decode("utf-8"))
f.close()
