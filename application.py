from flask import Flask
from flask import jsonify
from flask import Response
from flask_cors import CORS

import requests

class Device():
  def __init__(self, name, ID, lastSeen, created):
    self.name = name
    self.ID = ID
    self.lastSeen = lastSeen
    self.created = created

base_url = 'https://app.torizon.io/api/v2beta/'

log_file = 'tps-backend.log'

application = Flask(__name__)
CORS(application)

OAuth2Token = ""
def getOAuth2Token():
    global OAuth2Token
    url = 'https://kc.torizon.io/auth/realms/ota-users/protocol/openid-connect/token'
    header_data = {'content-type' : 'application/x-www-form-urlencoded'}
    oauth2specifics = {'grant_type' : 'client_credentials',
                       'client_id' : 'api-v2_4320be3d_cf952e08-daa8-410c-89b6-4bb888b64b88',
                       'client_secret' : 'F9KiHLCvuBIeuDjDiNelh3k1AUO0jYEH'
                      }
    response = requests.post(url, headers=header_data, data=oauth2specifics)
    json_response = response.json()
    OAuth2Token = json_response['access_token']

def getAllDevices():
    total_devices = []
    headers = {'Authorization' : 'Bearer ' + OAuth2Token}
    params = {'offset' : 0, 'limit' : 10 }
    url = base_url + 'devices/core'
    response = requests.get(url, params=params, headers=headers)
    json_response = response.json()
    with open(log_file, 'a') as f:
        f.write(str(json_response) + '\n')
    for device in json_response['values']:
      total_devices.append(Device(device['deviceName'], device['deviceId'], device['lastSeen'], device['createdAt'])) 
    return json_response

def addDevice():
    headers = {'Authorization' : 'Bearer ' + OAuth2Token}
    url = base_url + 'devices/core'

    response = requests.post(url, json={'deviceId': 'device1', 'deviceName': 'mabdevice'}, headers=headers)
    print("response = " + response.text)
    with open("provision.zip", "wb") as f:
      f.write(response.content)

@application.route('/get-auth', methods=["GET"])
def get_auth():
    getOAuth2Token()
    return '', 200

@application.route('/num-devices', methods=["GET"])
def num_devices():
    return getAllDevices()

if __name__ == "__main__":
    application.debug = True
    application.run()
