#! /usr/bin/env python3
import os
import requests
import json
from datetime import datetime, timezone
import subprocess

filepath = "coordinates.json"
infile = open(filepath, "r")
data = json.load(infile)
infile.close()

ref = f"https://api.sunrise-sunset.org/json"

params = {
    'lat': data["lat"],
    'lng': data["lng"],
    'date': 'tomorrow', 
    'formatted': 0
    }

r = requests.put(ref, params = params)
data = r.json()
time = data['results']['sunrise']
datetimeobj = datetime.fromisoformat(time)
localdatetimeobj = datetimeobj.astimezone()
hour = localdatetimeobj.hour
minute = localdatetimeobj.minute
second = localdatetimeobj.second
pattern = './wakeup.py'

bashCommand = f"crontab -l | sed -E \"\#{pattern}#{{s#^([^[:space:]]+[[:space:]]+[^[:space:]]+)#{minute} {hour}#;s#sleep[[:space:]]+[[:digit:]]+#sleep {second}#}}\" - | crontab -"

process = subprocess.run(bashCommand, shell=True, check=True, capture_output=True)