#! /usr/bin/env python3
import os
import requests
import json
from datetime import datetime
from datetime import timedelta

filepath = "tokens.json"
infile = open(filepath, "r")
data = json.load(infile)
infile.close()

expires = datetime.strptime(data["expires"], '%Y-%m-%d %H:%M:%S.%f')

if datetime.now() > expires:
    payload = {
        'grant_type':'refresh_token',
        'refresh_token':data["refresh_token"],
        'client_id':os.getenv('S_CLIENT_ID')
        }
    now = datetime.now()
    r = requests.post('https://accounts.spotify.com/api/token', data = payload)

    data = r.json()
    data = {
        'access_token':data["access_token"],
        'refresh_token':data["refresh_token"],
        'expires':str(now + timedelta(seconds = (data["expires_in"]) - 60))
        }

    data = json.dumps(data, indent=2)

    fo = open(filepath, "w")
    fo.write(data)
    fo.close()