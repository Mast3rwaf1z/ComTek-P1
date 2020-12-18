import requests
import json
import base64
import time

# This is the program used for the packet loss test

def get_jwt():
# Login credentials in JSON formatting
    data = {
        "email": "Email",
        "password": "Password"
    }

    response = requests.post('http://loratest.lanestolen.dk:8080/api/internal/login', data=json.dumps(data))    # Send a request to the server to login, send JSON data as JSON python object
    response_data = json.loads(response.content)                                        # Set the response of the request as a string
    if (response_data.get('jwt')):                                                      # If the login was successful the JSON data should contain the "jwt" entry
        print('Login Success')
        return response_data.get('jwt')                                                 # Return the token to use it in later code
    else:
        print('Login Failed')
        return False                                                                    # Return False if it wasn't possible to login

# -----------------------------------------Globally set up header and body--------------------------------------------

# Different requests url's that are being used later in the program
mc_queue_url = 'http://loratest.lanestolen.dk:8080/api/multicast-groups/929e121c-f2d2-48cd-b1ff-94684d226b41/queue'
d_queue_url = 'http://loratest.lanestolen.dk:8080/api/devices/70B3D54993383389/queue'
d_queue_flush_url = 'http://loratest.lanestolen.dk:8080/api/devices/70B3D54993383389/queue'
# Package data
body = {
  "deviceQueueItem": {
    "confirmed": False,
    "data": [],
    "devEUI": "70B3D54993383389",
    "fCnt": 0,
    "fPort": 1
  }
}
# Header
headers = {'content-type': 'application/json',"Grpc-Metadata-Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJjaGlycHN0YWNrLWFwcGxpY2F0aW9uLXNlcnZlciIsImV4cCI6MTYwNTg3OTA5MywiaWQiOjMsImlzcyI6ImNoaXJwc3RhY2stYXBwbGljYXRpb24tc2VydmVyIiwibmJmIjoxNjA1NzkyNjkzLCJzdWIiOiJ1c2VyIiwidXNlcm5hbWUiOiJzanVobDIwQHN0dWRlbnQuYWF1LmRrIn0.xUbcFNbpLuQFzyz_CLBrtP3Qzk4sd6LGwmP-Iba-EdY"}

headers['Grpc-Metadata-Authorization'] = "Bearer " + get_jwt()

# -------------------------------------------------------------------------------------------------------------------

# These test packets are actual encoded packets
Test_Packet = [2, 65, 233, 94, 32, 40, 29, 154, 179, 131, 149, 237, 97, 184, 243, 247, 135, 64, 91, 216, 166, 53, 64, 147, 171, 25, 11, 60, 106, 143, 226, 36, 142, 121, 231, 110, 85, 242, 163, 155, 49, 141, 173, 8, 115, 228, 216, 165, 57, 106]
Test_Packet2 = [2, 65, 233, 114, 19, 40, 5, 16, 146, 33, 242, 75, 250, 250, 94, 233, 84, 29, 143, 33, 82, 196, 112, 23, 8, 125, 224, 56, 63, 230, 145, 140, 123, 53, 158, 8, 146, 157, 89, 62, 245, 246, 228, 11, 225, 227, 81, 85, 230]

requests.delete(d_queue_flush_url, headers=headers)                                 # Send a request to flush the downlink queue
print("Queue flushed")                                                              # Print a feedback message
time.sleep(1)                                                                       # Wait a second, so it is possible to flush the queue without sending packets

for i in range(64):                                                                 # Range of the loop decides the number of packets to be sent
        if not i % 2:                                                               # If i is even
            Packet = Test_Packet                                                    # Send first test packet
        else:                                                                       # Else if i is odd
            Packet = Test_Packet2                                                   # Send second test packet
        base64_bytes = base64.b64encode(bytearray(Packet))                          # Encode packet in Base64
        base64_message = base64_bytes.decode('ascii')                               # Encode the Base64 packet in Ascii
        body['deviceQueueItem']['data'] = base64_message                            # Set the Base64 Ascii string as the data to be sent
        r = requests.post(d_queue_url, data=json.dumps(body), headers=headers)      # Send a post request to send the packet
        print("Packet " + str(i) + " Sent")                                         # Print a feedback message
        print(Packet)                                                               # Print the packet that was sent
