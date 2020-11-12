import json
import os
import sys
import requests


with open('login.json') as file:
    login = json.load(file)

with open('headers.json') as file:
    headers = json.load(file)

def getJWT():
    response = requests.post('http://loratest.lanestolen.dk:8080/api/internal/login',data=json.dumps(login), headers=headers)
    response_data = json.loads(response.content)
    if (response_data.get('jwt')):
        headers['Authorization'] = response_data.get('jwt')
        return response_data.get('jwt')
    else:
        headers['Authorization'] = 'invalid'
        return False
def post(addr, data):
    response = requests.post(addr,data=json.dumps(data), headers=headers)
    response_data = json.loads(response.content)
    return response_data    
def get(addr):
    get_app = requests.get(addr, headers=headers)
    return get_app

response = post('http://loratest.lanestolen.dk:8080/api/internal/login',json.load(open("login.json")))
if (response.get('jwt')):
    headers['Grpc-Metadata-Authorization'] = response.get('jwt')
    print(headers['Grpc-Metadata-Authorization'])
    with open('headers.json', 'w') as target:
        json.dump(headers, target, indent=4)

devices=json.loads(get("http://loratest.lanestolen.dk:8080/api/devices?limit=8").content)
#print(json.dumps(devices,indent=2))
