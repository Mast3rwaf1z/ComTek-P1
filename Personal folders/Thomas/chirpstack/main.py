import json
import requests

with open('login.json') as file:                    
    login = json.load(file)

with open('headers.json') as file:
    headers = json.load(file)

with open("data.json") as file:
    data = json.load(file)

with open("devData.json") as file:
    devData = json.load(file)

def post(addr, data):
    response = requests.post(addr,data=json.dumps(data), headers=headers)
    response_data = json.loads(response.content)
    return response_data    
def get(addr):
    response = requests.get(addr, headers=headers)
    Json = response.content
    return Json
#get a new JWT token and save it in a json file
response = post('http://loratest.lanestolen.dk:8080/api/internal/login', login)
if (response.get('jwt')):
    headers['Grpc-Metadata-Authorization'] = response.get('jwt')
    print(json.dumps(headers, indent=4))
    with open('headers.json', 'w') as target:
        json.dump(headers, target, indent=4)

print()
#enqueue data in multicast a set number of times, print response
for i in range(300):
    response = post("http://loratest.lanestolen.dk:8080/api/multicast-groups/929e121c-f2d2-48cd-b1ff-94684d226b41/queue", data)
    #response = post("http://loratest.lanestolen.dk:8080/api/devices/70b3d54993383389/queue", devData)
    print(json.dumps(response, indent=4))

print()

#get the queue
#queue = get("http://loratest.lanestolen.dk:8080/api/multicast-groups/929e121c-f2d2-48cd-b1ff-94684d226b41/queue")
#print(json.dumps(queue))