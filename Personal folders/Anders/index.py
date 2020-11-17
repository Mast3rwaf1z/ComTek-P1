import requests
import json

headers = {

}

data = {
  "email": "sjuhl20@student.aau.dk",
  "password": "wWnxiryiCBtU3Ta"
}

r = requests.post("http://loratest.lanestolen.dk:8080/api/internal/login", data=json.dumps(data))
response = json.loads(r.content)

if (response.get('jwt')):
    print('Login Success')
else:
    print('Login Failed')
    
headers['Grpc-Metadata-Authorization'] = response.get('jwt') 

gw_list = requests.get('http://loratest.lanestolen.dk:8080/api/gateways',headers=headers)
gw_response = json.loads(gw_list.content)
print(gw_response)

gw_profile = requests.get('http://loratest.lanestolen.dk:8080/api/gateway-profiles/dca632fffe5498ca', headers=headers)
gw_data = json.loads(gw_profile.content)
print(gw_data)

if __name__ == '__index__':
    index()

