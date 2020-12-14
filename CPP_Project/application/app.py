import os
from flask import Flask, render_template, request, redirect, send_file, url_for
from s3 import list_files, download_file, upload_file
from dynamodb import db_put_team_item, db_put_player_item, db_scan_items
from flask_bootstrap import Bootstrap
import json
from colours import ColourGenerator

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
BUCKET = "rb-test-myapp-bucket"
dynamoTeamsTable = 'Premier-League-Teams'
dynamoPlayersTable = 'Premier-League-Players'
bootstrap = Bootstrap(app)


@app.route('/')
def entry_point():
 
    table = None
    cg = ColourGenerator()
    table = db_scan_items(dynamoTeamsTable)

    contents = []
    if table is None:
        pass
    else:
        teamsList = []
        for i in table['Items']:
            teamsList.append(i['Team'])
           
        results = cg.getPremierLeagueColoursRGBA(teamsList)
        teamsList = results
        
        uniqueTeamsList = []     
        for j in teamsList:
            dict = {}
            if j not in uniqueTeamsList:
                dict['team'] = j['team']
                dict['colour'] = j['colour']
                dict['count'] = teamsList.count(j)
                uniqueTeamsList.append(dict)
    
        chartSet = set()
        for d in uniqueTeamsList:
            if d['team'] not in chartSet:
                chartSet.add(d['team'])
                contents.append(d)            
        
    return render_template('main.html', contents=contents)
    
    
@app.route('/teams')
def teams():
    contents = []
    with open('leagueTable.json') as json_file:
        data = json.load(json_file)
        i = 1
        for p in data['records']:
            dict = {}
            dict['team'] = p['team']
            dict['position'] = i
            dict['played'] = p['played']
            dict['points'] = p['points']
            contents.append(dict)
            i += 1
    
    return render_template('teams.html', contents=contents)


@app.route("/team", methods=['POST'])
def uploadTeamEntry():
    if request.method == "POST":
        team = request.form['team']
        db_put_team_item(team, dynamoTeamsTable)
    
        return render_template('thanks.html',msg = team)
        
        
@app.route('/players')
def players():
    return render_template('players.html')


@app.route("/player", methods=['POST'])
def uploadPlayerEntry():
    if request.method == "POST":
        player = request.form['player']
        db_put_player_item(player, dynamoPlayersTable)
    
        return render_template('thanks.html',msg = player)


@app.route("/storage")
def storage():
   contents = list_files(BUCKET)
   return render_template('storage.html', contents=contents)


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')


@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        if request.files['file']:
            f = request.files['file']
            f.save(f.filename)
            upload_file(f"{f.filename}", BUCKET)

        return redirect("/storage")


@app.route("/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8080, debug=True)
