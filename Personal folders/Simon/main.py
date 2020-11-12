import requests
import json
from datetime import datetime

gw_info = None

headers = {
    # 'Content-Type' : 'application/json',
    # 'Accept' : 'application/json'
    # 'Grpc-Metadata-Authorization' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJjaGlycHN0YWNrLWFwcGxpY2F0aW9uLXNlcnZlciIsImV4cCI6MTYwNTA4NDY2OCwiaWQiOjMsImlzcyI6ImNoaXJwc3RhY2stYXBwbGljYXRpb24tc2VydmVyIiwibmJmIjoxNjA0OTk4MjY4LCJzdWIiOiJ1c2VyIiwidXNlcm5hbWUiOiJzanVobDIwQHN0dWRlbnQuYWF1LmRrIn0.nGOprXS22DU-7Z3YPl_v6VcYWtlcsGRSMjcuNjHmqu4'
}

def get_jwt():
    data = {
        "email": "sjuhl20@student.aau.dk",
        "password": "wWnxiryiCBtU3Ta"
    }

    response = requests.post('http://loratest.lanestolen.dk:8080/api/internal/login', headers=headers, data=json.dumps(data))
    response_data = json.loads(response.content)
    if (response_data.get('jwt')):
        headers['Grpc-Metadata-Authorization'] = response_data.get('jwt')
        print('Login Success')
        return response_data.get('jwt')
    else:
        print('Login Failed')
        return False

def find_gateway():
    get_app = requests.get('http://loratest.lanestolen.dk:8080/api/gateways?limit=1&search=dca', headers=headers)
    return get_app.content

def main():
    print('\nJWT: ' + get_jwt())
    gw_info = json.dumps(json.loads(find_gateway()), indent=2)
    print('\nGateway: ' + gw_info)

if __name__ == '__main__':
    main()
