{"filter":false,"title":"application.py","tooltip":"/Project/application.py","undoManager":{"mark":18,"position":18,"stack":[[{"start":{"row":0,"column":0},"end":{"row":33,"column":21},"action":"insert","lines":["from flask import Flask","","# print a nice greeting.","def say_hello(username = \"World\"):","    return '<p>Hello %s!</p>\\n' % username","","# some bits of text for the page.","header_text = '''","    <html>\\n<head> <title>EB Flask Test</title> </head>\\n<body>'''","instructions = '''","    <p><em>Hint</em>: This is a RESTful web service! Append a username","    to the URL (for example: <code>/Thelonious</code>) to say hello to","    someone specific.</p>\\n'''","home_link = '<p><a href=\"/\">Back</a></p>\\n'","footer_text = '</body>\\n</html>'","","# EB looks for an 'application' callable by default.","application = Flask(__name__)","","# add a rule for the index page.","application.add_url_rule('/', 'index', (lambda: header_text +","    say_hello() + instructions + footer_text))","","# add a rule when the page is accessed with a name appended to the site","# URL.","application.add_url_rule('/<username>', 'hello', (lambda username:","    header_text + say_hello(username) + home_link + footer_text))","","# run the app.","if __name__ == \"__main__\":","    # Setting debug to True enables debug output. This line should be","    # removed before deploying a production app.","    application.debug = True","    application.run()"],"id":1}],[{"start":{"row":0,"column":0},"end":{"row":26,"column":65},"action":"remove","lines":["from flask import Flask","","# print a nice greeting.","def say_hello(username = \"World\"):","    return '<p>Hello %s!</p>\\n' % username","","# some bits of text for the page.","header_text = '''","    <html>\\n<head> <title>EB Flask Test</title> </head>\\n<body>'''","instructions = '''","    <p><em>Hint</em>: This is a RESTful web service! Append a username","    to the URL (for example: <code>/Thelonious</code>) to say hello to","    someone specific.</p>\\n'''","home_link = '<p><a href=\"/\">Back</a></p>\\n'","footer_text = '</body>\\n</html>'","","# EB looks for an 'application' callable by default.","application = Flask(__name__)","","# add a rule for the index page.","application.add_url_rule('/', 'index', (lambda: header_text +","    say_hello() + instructions + footer_text))","","# add a rule when the page is accessed with a name appended to the site","# URL.","application.add_url_rule('/<username>', 'hello', (lambda username:","    header_text + say_hello(username) + home_link + footer_text))"],"id":2},{"start":{"row":0,"column":0},"end":{"row":165,"column":52},"action":"insert","lines":["import os","from flask import Flask, render_template, request, redirect, send_file, url_for","from s3 import list_files, download_file, upload_file","from dynamodb import db_put_team_item, db_put_player_item, db_scan_items","from flask_bootstrap import Bootstrap","import json","from datetime import date","#from colours import ColourGenerator","from colour_generator_pkg import colours","","application = Flask(__name__)","UPLOAD_FOLDER = \"uploads\"","BUCKET = \"rb-pl-voting-app-images\" # rb-test-myapp-bucket","dynamoTeamsTable = 'Premier-League-Teams'","dynamoPlayersTable = 'Premier-League-Players'","bootstrap = Bootstrap(application)","","","@application.route('/')","def entry_point():"," ","    table = None","    #cg = ColourGenerator()","    cg = colours.ColourGenerator()","    table = db_scan_items(dynamoTeamsTable)","","    contents = []","    if table is None:","        pass","    else:","        teamsList = []","        for i in table['Items']:","            teamsList.append(i['Team'])","           ","        results = cg.getPremierLeagueColoursRGBA(teamsList)","        teamsList = results","        ","        uniqueTeamsList = []     ","        for j in teamsList:","            dict = {}","            if j not in uniqueTeamsList:","                dict['team'] = j['team']","                dict['colour'] = j['colour']","                dict['count'] = teamsList.count(j)","                uniqueTeamsList.append(dict)","    ","        chartSet = set()","        for d in uniqueTeamsList:","            if d['team'] not in chartSet:","                chartSet.add(d['team'])","                contents.append(d)            ","        ","    return render_template('main.html', contents=contents)","    ","    ","@application.route('/teams')","def teams():","    contents = []","    with open('leagueTable.json') as json_file:","        data = json.load(json_file)","        i = 1","        for p in data['records']:","            dict = {}","            dict['team'] = p['team']","            dict['position'] = i","            dict['played'] = p['played']","            dict['points'] = p['points']","            contents.append(dict)","            i += 1","    ","    return render_template('teams.html', contents=contents)","","","@application.route(\"/team\", methods=['POST'])","def uploadTeamEntry():","    if request.method == \"POST\":","        team = request.form['team']","        email = request.form['email']","        isEmail = False","        isToday = False","        ","        if email != \"\":","            response = db_scan_items(dynamoTeamsTable)","            ","            for i in response['Items']:","                for key, value in i.items():","                    if str(key) == 'Email' and str(value) == email:","                        isEmail = True","                    if str(key) == 'Datetime' and str(value) == date.today().strftime(\"%d/%m/%Y\"):","                        isToday = True","   ","            if isEmail and isToday:","                msg = \"Sorry :( You can only vote once a day\"","                return render_template('thanks.html',msg = msg)","            else:","                db_put_team_item(team, email, dynamoTeamsTable)","                return render_template('thanks.html',msg = team)","            ","        else:","            msg = \"Please enter your email address and try again\"","            return render_template('thanks.html',msg = msg)","        ","        ","@application.route('/players')","def players():","    return render_template('players.html')","","","@application.route(\"/player\", methods=['POST'])","def uploadPlayerEntry():","    if request.method == \"POST\":","        player = request.form['player']","        email = request.form['email']","        isEmail = False","        isToday = False","        ","        if email != \"\":","            response = db_scan_items(dynamoPlayersTable)","            ","            for i in response['Items']:","                for key, value in i.items():","                    if str(key) == 'Email' and str(value) == email:","                        isEmail = True","                    if str(key) == 'Datetime' and str(value) == date.today().strftime(\"%d/%m/%Y\"):","                        isToday = True","   ","            if isEmail and isToday:","                msg = \"Sorry :( You can only vote once a day\"","                return render_template('thanks.html',msg = msg)","            else:","                db_put_player_item(player, email, dynamoPlayersTable)","                return render_template('thanks.html',msg = player)","            ","        else:","            msg = \"Please enter your email address and try again\"","            return render_template('thanks.html',msg = msg)","","","@application.route(\"/images\")","def storage():","   contents = list_files(BUCKET)","   return render_template('storage.html', contents=contents)","","","@application.route('/message')","def thanks():","    return render_template('thanks.html')","","","@application.route(\"/upload\", methods=['POST'])","def upload():","    if request.method == \"POST\":","        if request.files['file']:","            f = request.files['file']","            f.save(f.filename)","            upload_file(f\"{f.filename}\", BUCKET)","","        return redirect(\"/images\")","","","@application.route(\"/<filename>\", methods=['GET'])","def download(filename):","    if request.method == 'GET':","        output = download_file(filename, BUCKET)","","        return send_file(output, as_attachment=True)"]}],[{"start":{"row":20,"column":1},"end":{"row":21,"column":0},"action":"insert","lines":["",""],"id":3},{"start":{"row":21,"column":0},"end":{"row":21,"column":1},"action":"insert","lines":[" "]}],[{"start":{"row":21,"column":1},"end":{"row":21,"column":4},"action":"insert","lines":["   "],"id":4}],[{"start":{"row":21,"column":4},"end":{"row":21,"column":8},"action":"insert","lines":["try:"],"id":5}],[{"start":{"row":20,"column":1},"end":{"row":21,"column":0},"action":"insert","lines":["",""],"id":6},{"start":{"row":21,"column":0},"end":{"row":21,"column":1},"action":"insert","lines":[" "]}],[{"start":{"row":21,"column":1},"end":{"row":21,"column":4},"action":"insert","lines":["   "],"id":7}],[{"start":{"row":21,"column":4},"end":{"row":21,"column":17},"action":"insert","lines":["contents = []"],"id":8}],[{"start":{"row":21,"column":17},"end":{"row":22,"column":0},"action":"insert","lines":["",""],"id":9},{"start":{"row":22,"column":0},"end":{"row":22,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":29,"column":0},"end":{"row":29,"column":17},"action":"remove","lines":["    contents = []"],"id":10},{"start":{"row":28,"column":0},"end":{"row":29,"column":0},"action":"remove","lines":["",""]}],[{"start":{"row":24,"column":0},"end":{"row":24,"column":4},"action":"insert","lines":["    "],"id":11},{"start":{"row":25,"column":0},"end":{"row":25,"column":4},"action":"insert","lines":["    "]},{"start":{"row":26,"column":0},"end":{"row":26,"column":4},"action":"insert","lines":["    "]},{"start":{"row":27,"column":0},"end":{"row":27,"column":4},"action":"insert","lines":["    "]},{"start":{"row":28,"column":0},"end":{"row":28,"column":4},"action":"insert","lines":["    "]},{"start":{"row":29,"column":0},"end":{"row":29,"column":4},"action":"insert","lines":["    "]},{"start":{"row":30,"column":0},"end":{"row":30,"column":4},"action":"insert","lines":["    "]},{"start":{"row":31,"column":0},"end":{"row":31,"column":4},"action":"insert","lines":["    "]},{"start":{"row":32,"column":0},"end":{"row":32,"column":4},"action":"insert","lines":["    "]},{"start":{"row":33,"column":0},"end":{"row":33,"column":4},"action":"insert","lines":["    "]},{"start":{"row":34,"column":0},"end":{"row":34,"column":4},"action":"insert","lines":["    "]},{"start":{"row":35,"column":0},"end":{"row":35,"column":4},"action":"insert","lines":["    "]},{"start":{"row":36,"column":0},"end":{"row":36,"column":4},"action":"insert","lines":["    "]},{"start":{"row":37,"column":0},"end":{"row":37,"column":4},"action":"insert","lines":["    "]},{"start":{"row":38,"column":0},"end":{"row":38,"column":4},"action":"insert","lines":["    "]},{"start":{"row":39,"column":0},"end":{"row":39,"column":4},"action":"insert","lines":["    "]},{"start":{"row":40,"column":0},"end":{"row":40,"column":4},"action":"insert","lines":["    "]},{"start":{"row":41,"column":0},"end":{"row":41,"column":4},"action":"insert","lines":["    "]},{"start":{"row":42,"column":0},"end":{"row":42,"column":4},"action":"insert","lines":["    "]},{"start":{"row":43,"column":0},"end":{"row":43,"column":4},"action":"insert","lines":["    "]},{"start":{"row":44,"column":0},"end":{"row":44,"column":4},"action":"insert","lines":["    "]},{"start":{"row":45,"column":0},"end":{"row":45,"column":4},"action":"insert","lines":["    "]},{"start":{"row":46,"column":0},"end":{"row":46,"column":4},"action":"insert","lines":["    "]},{"start":{"row":47,"column":0},"end":{"row":47,"column":4},"action":"insert","lines":["    "]},{"start":{"row":48,"column":0},"end":{"row":48,"column":4},"action":"insert","lines":["    "]},{"start":{"row":49,"column":0},"end":{"row":49,"column":4},"action":"insert","lines":["    "]},{"start":{"row":50,"column":0},"end":{"row":50,"column":4},"action":"insert","lines":["    "]},{"start":{"row":51,"column":0},"end":{"row":51,"column":4},"action":"insert","lines":["    "]},{"start":{"row":52,"column":0},"end":{"row":52,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":53,"column":8},"end":{"row":54,"column":0},"action":"insert","lines":["",""],"id":12},{"start":{"row":54,"column":0},"end":{"row":54,"column":8},"action":"insert","lines":["        "]}],[{"start":{"row":53,"column":4},"end":{"row":53,"column":8},"action":"remove","lines":["    "],"id":13}],[{"start":{"row":53,"column":4},"end":{"row":53,"column":5},"action":"insert","lines":["e"],"id":14},{"start":{"row":53,"column":5},"end":{"row":53,"column":6},"action":"insert","lines":["x"]},{"start":{"row":53,"column":6},"end":{"row":53,"column":7},"action":"insert","lines":["c"]},{"start":{"row":53,"column":7},"end":{"row":53,"column":8},"action":"insert","lines":["e"]},{"start":{"row":53,"column":8},"end":{"row":53,"column":9},"action":"insert","lines":["p"]},{"start":{"row":53,"column":9},"end":{"row":53,"column":10},"action":"insert","lines":["t"]}],[{"start":{"row":53,"column":4},"end":{"row":53,"column":10},"action":"remove","lines":["except"],"id":15},{"start":{"row":53,"column":4},"end":{"row":54,"column":16},"action":"insert","lines":["except Exception as e:","        print(e)"]}],[{"start":{"row":144,"column":30},"end":{"row":144,"column":31},"action":"remove","lines":["T"],"id":16},{"start":{"row":144,"column":29},"end":{"row":144,"column":30},"action":"remove","lines":["E"]},{"start":{"row":144,"column":28},"end":{"row":144,"column":29},"action":"remove","lines":["K"]},{"start":{"row":144,"column":27},"end":{"row":144,"column":28},"action":"remove","lines":["C"]},{"start":{"row":144,"column":26},"end":{"row":144,"column":27},"action":"remove","lines":["U"]},{"start":{"row":144,"column":25},"end":{"row":144,"column":26},"action":"remove","lines":["B"]}],[{"start":{"row":144,"column":25},"end":{"row":144,"column":27},"action":"insert","lines":["\"\""],"id":17}],[{"start":{"row":144,"column":26},"end":{"row":144,"column":27},"action":"insert","lines":["r"],"id":18}],[{"start":{"row":144,"column":27},"end":{"row":144,"column":49},"action":"insert","lines":["b-pl-voting-app-images"],"id":19}]]},"ace":{"folds":[],"scrolltop":1799,"scrollleft":0,"selection":{"start":{"row":160,"column":0},"end":{"row":160,"column":0},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1608155482868,"hash":"785fb898c987c95cdef9c6220b2924f4bc947ced"}