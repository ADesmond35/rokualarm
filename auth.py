#! /usr/bin/env python3
import os
import re
import string
import hashlib
import base64
from urllib.parse import urlencode
import requests
import json
from datetime import datetime
from datetime import timedelta

code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
code_verifier = re.sub('[^a-zA-Z0-9.~_-]+', '', code_verifier)
code_verifier_sha256 = hashlib.sha256(code_verifier.encode('utf-8'))
code_challenge = base64.urlsafe_b64encode(code_verifier_sha256.digest()).decode('utf-8')
code_challenge = code_challenge.replace('=', '')

client_id = os.getenv('S_CLIENT_ID')
redirect_uri = "https://adesmond.codes"

payload = {
    'response_type':'code',
    'client_id':client_id,
    'redirect_uri':redirect_uri,
    'scope':'user-read-playback-state user-modify-playback-state playlist-read-private playlist-read-collaborative',
    'code_challenge':code_challenge,
    'code_challenge_method':'S256'
    }

auth_uri = "https://accounts.spotify.com/authorize?" + urlencode(payload)
print("auth URI: " + auth_uri)
auth_code = input("Enter auth code: ")

payload = {
    'client_id':client_id,
    'grant_type':'authorization_code',
    'code':auth_code,
    'redirect_uri':redirect_uri,
    'code_verifier':code_verifier
    }
expires = datetime.now()
r = requests.post('https://accounts.spotify.com/api/token', data = payload)
data = r.json()
expires = str(expires + timedelta(seconds = (data["expires_in"]) - 5))
data = {
    'access_token':data["access_token"],
    'refresh_token':data["refresh_token"],
    'expires':expires
    }
data = json.dumps(data, indent=2)

fo = open("tokens.json", "w")
fo.write(data)
fo.close()
