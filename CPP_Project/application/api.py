#import http.client
from colours import ColourGenerator

data = []

cg = ColourGenerator()

n = cg.getPremierLeagueColours(data)

print(n)

'''
conn = http.client.HTTPSConnection("heisenbug-premier-league-live-scores-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "",
    'x-rapidapi-host': "heisenbug-premier-league-live-scores-v1.p.rapidapi.com"
    }

conn.request("GET", "/api/premierleague/table", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
'''