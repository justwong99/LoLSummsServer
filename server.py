#!flask/bin/python

import requests
import json
from flask import jsonify
from flask import jsonify,make_response
from flask import Flask
from flask import request
app = Flask(__name__)


@app.route("/info")
def info():
    blue = False
    sideNum = 0
    name = request.args.get('name')
    name.replace(" ", "")
    region = request.args.get('region')
    api_key = "RGAPI-eccf9810-f60f-43a9-8ba7-564207195542"
    api_url = "https://" + region + ".api.riotgames.com/lol/summoner/v3/summoners/by-name/" + name + "?api_key=" + api_key 
    response = requests.get(api_url)
    summ_id = json.dumps(response.json()['id'])
    api_url2 = "https://" + region + ".api.riotgames.com/lol/spectator/v3/active-games/by-summoner/" + summ_id + "?api_key=" + api_key
    response2 = requests.get(api_url2)
    summoners = [["" for x in range(4)] for y in range(5)]
    for i in range (5):
        randomName = ((response2.json()['participants'][i]['summonerName']).lower()).replace(" ","")
        if (randomName == name):
            blue = True
    if blue == True:
        sideNum = 5
    for i in range (5):
        tempMasteries = []
        summoners[i][0] = response2.json()['participants'][i + sideNum]['championId']
        summoners[i][1] = response2.json()['participants'][i + sideNum]['spell1Id']
        summoners[i][2] = response2.json()['participants'][i + sideNum]['spell2Id']
        for k in range (len(response2.json()['participants'][i + sideNum]['masteries'])):
            tempMasteries.append(response2.json()['participants'][i + sideNum]['masteries'][k]['masteryId'])
        for k in range (len(response2.json()['participants'][i + sideNum]['masteries'])):
            if tempMasteries[k] == 6241:
                summoners[i][3] = 1
        if (summoners[i][3] != 1):
            summoners[i][3] = 0

            
    ingame_info = json.dumps(summoners)
    return ingame_info


if __name__ == '__main__':
    app.run(debug=True)


