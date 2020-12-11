import os

from flask import Flask, render_template, request, redirect, send_file, url_for

from s3 import list_files, download_file, upload_file

from flask_bootstrap import Bootstrap

import boto3

import uuid

import json

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
BUCKET = "rb-test-myapp-bucket"
dynamodb = boto3.resource('dynamodb')
dynamoTeamsTable = dynamodb.Table('Premier-League-Teams')
dynamoPlayersTable = dynamodb.Table('Premier-League-Players')
bootstrap = Bootstrap(app)


@app.route('/')
def entry_point():
    return render_template('main.html')
    #return 'Hello World!'


@app.route('/teams')
def teams():
    contents = []
    with open('leagueTable.json') as json_file:
        data = json.load(json_file)
        for p in data['records']:
            contents.append(p['team'])
            print(p['team'])
    
    print(contents)
    return render_template('teams.html', contents=contents)


@app.route("/team", methods=['POST'])
def uploadTeamEntry():
    if request.method == "POST":
        
        team = request.form['team']
        
        dynamoTeamsTable.put_item(
            Item={
                'ID': str(uuid.uuid4()),
                'Team':team
            }
        )
        
        msg = "Thanks for voting "+team+" as your favourite team!"
    
        return render_template('main.html',msg = msg)
        
        
@app.route('/players')
def players():
    return render_template('players.html')
    '''
    contents = []
    with open('leagueTable.json') as json_file:
        data = json.load(json_file)
        for p in data['records']:
            contents.append(p['team'])
            print(p['team'])
    
    print(contents)
    return render_template('players.html', contents=contents)
    '''


@app.route("/player", methods=['POST'])
def uploadPlayerEntry():
    if request.method == "POST":
        
        player = request.form['player']
        
        dynamoPlayersTable.put_item(
            Item={
                'ID': str(uuid.uuid4()),
                'Player':player
            }
        )
        
        msg = "Thanks for voting "+player+" as your favourite player!"
    
        return render_template('main.html',msg = msg)


@app.route("/storage")
def storage():
   contents = list_files(BUCKET)
   return render_template('storage.html', contents=contents)


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
