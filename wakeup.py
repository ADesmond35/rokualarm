#! /bin/python3
import os
import requests
import json
import time
import refresh_tokens
from datetime import datetime

filepath = "tokens.json"
infile = open(filepath, 'r')
data = json.load(infile)
infile.close()

#print("rise and shine here's some jacob collier")

#import environment variables
DEVICE_ID = os.getenv('ROKU_DEVICE_ID')
ROKU_ADDRESS = os.getenv('ROKU_DEV_TARGET')
PLAYLIST_URI = os.getenv('WAKEUP_PLAYLIST_URI')

print(datetime.now())

#Turn on the TV
ref = f"http://{ROKU_ADDRESS}:8060/keypress/poweron"
#print("ref:",ref)
r = requests.post(ref)

HEADERS = {
    'Accept': 'application/json',
    'Content-Type':'application/json',
    'Authorization': 'Bearer {}'.format(data['access_token'])
}
#print(f"Headers: {HEADERS}")

#get available devices
if False:
    ref = 'https://api.spotify.com/v1/me/player/devices'
    r = requests.get(ref, headers = HEADERS)
    data = r.json()
    print(data)
    #"id": "84d00fde-f612-5eba-9bce-f1800e30aef5"

#transfer playback
if True:
    ref = 'https://api.spotify.com/v1/me/player'
    payload = {
        'device_ids':[DEVICE_ID],
        'play':False
        }
    time.sleep(1)
    attempts = 0
    #print(json.dumps(payload))
    while True: #do while loop
        r = requests.put(ref, headers = HEADERS, json = payload)
        if r.status_code == 204 or attempts > 9:
            print(f"Transferred playback")
            #time.sleep(1)
            break
        print(f"Transfer playback failed, Response text: \n{r.text}")
        attempts += 1
        time.sleep(3)

#Toggle Shuffle For User’s Playback
if True:
    ref = 'https://api.spotify.com/v1/me/player/shuffle'
    params = {
        'state': 'true',
        'device_id': DEVICE_ID
    }
    r = requests.put(ref, headers = HEADERS, params = params)
    if r.status_code == 204:
        print("Shuffle on")
    else:
        print(f"Shuffle toggle failed, Response text: \n{r.text}")

#Set Volume For User's Playback
if True:
    ref = 'https://api.spotify.com/v1/me/player/volume'
    params = {
        'volume_percent': '9',
        'device_id': DEVICE_ID
    }
    r = requests.put(ref, headers = HEADERS, params = params)
    if r.status_code == 204:
        print("Volume set")
    else:
        print(f"Volume setting failed, Response text: \n{r.text}")


#Set Repeat Mode On User’s Playback
if True:
    ref = 'https://api.spotify.com/v1/me/player/repeat'
    params = {
        'state': 'context',
        'device_id': DEVICE_ID
    }
    r = requests.put(ref, headers = HEADERS, params = params)
    if r.status_code == 204:
        print("Repeat mode set")
    else:
        print(f"Repeat mode setting failed, Response text: \n{r.text}")

#begin playback
if True:
    ref = 'https://api.spotify.com/v1/me/player/play'
    params = {
        'device_id': DEVICE_ID
    }
    payload = {
        'context_uri': PLAYLIST_URI
    }
    attempts = 0
    while True: #do while loop
        r = requests.put(ref, headers = HEADERS, params = params, json = payload)
        if r.status_code == 204 or attempts > 9:
            print(f"Playback started")
            break
        print(f"Playback start failed, Response text: \n{r.text}")
        attempts += 1
        time.sleep(3)
