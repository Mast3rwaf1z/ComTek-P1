import requests
import json
import base64
import binascii
import time
from datetime import datetime
from File_Splitting import *
from Encode_Symbol import Encode_Symbol
from Random_Matrix import Random_1D_Bit_Matrix

Send_Setup = 0                                                                                              # Will remember the use for this one day

def Get_Enc_Packet(Generation, File_Size, Gen_Num, density = 0.1):
    Enc_Vec = Random_1D_Bit_Matrix(len(Generation), density)
    while Enc_Vec == -1:
        Enc_Vec = Random_1D_Bit_Matrix(len(Generation), density)
    Enc_Pack = Encode_Symbol(Generation, Enc_Vec, File_Size, Gen_Num)
    return Enc_Pack

def Get_Enc_Packet_Pre_Defined_Enc_Vec(Generation, Enc_Vec, File_Size, Gen_Num):
    Enc_Pack = Encode_Symbol(Generation, Enc_Vec, File_Size, Gen_Num)
    return Enc_Pack

def get_jwt():

    data = {
        "email": "sjuhl20@student.aau.dk",
        "password": "wWnxiryiCBtU3Ta"
    }

    response = requests.post('http://loratest.lanestolen.dk:8080/api/internal/login', data=json.dumps(data))
    response_data = json.loads(response.content)
    if (response_data.get('jwt')):
        print('Login Success')
        return response_data.get('jwt')
    else:
        print('Login Failed')
        return False

# -----------------------------------------Globally set up header and body--------------------------------------------

mc_queue_url = 'http://loratest.lanestolen.dk:8080/api/multicast-groups/929e121c-f2d2-48cd-b1ff-94684d226b41/queue'
d_queue_url = 'http://loratest.lanestolen.dk:8080/api/devices/70B3D54993383389/queue'
d_queue_flush_url = 'http://loratest.lanestolen.dk:8080/api/devices/70B3D54993383389/queue'
body = {
  #"multicastQueueItem": {
  #  "data": [],
  #  "fPort": 1,
  #  "multicastGroupID": "929e121c-f2d2-48cd-b1ff-94684d226b41"
  #},
  "deviceQueueItem": {
    "confirmed": False,
    "data": [],
    "devEUI": "70B3D54993383389",
    "fCnt": 0,
    "fPort": 1
  }
}
headers = {'content-type': 'application/json',"Grpc-Metadata-Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJjaGlycHN0YWNrLWFwcGxpY2F0aW9uLXNlcnZlciIsImV4cCI6MTYwNTg3OTA5MywiaWQiOjMsImlzcyI6ImNoaXJwc3RhY2stYXBwbGljYXRpb24tc2VydmVyIiwibmJmIjoxNjA1NzkyNjkzLCJzdWIiOiJ1c2VyIiwidXNlcm5hbWUiOiJzanVobDIwQHN0dWRlbnQuYWF1LmRrIn0.xUbcFNbpLuQFzyz_CLBrtP3Qzk4sd6LGwmP-Iba-EdY"}

headers['Grpc-Metadata-Authorization'] = "Bearer " + get_jwt()

#print(headers['Grpc-Metadata-Authorization'])

# ------------------------------------------------Make Generation list globally---------------------------------------

#File = open("C:\\Users\moham\Desktop\LoPy files\main to decode.py","rb+")
File = open("C:\\Users\moham\Desktop\LoPy files\main2.py","rb+")
#File = open("C:\\Users\moham\Desktop\Gimp\Knuckeles.png","rb+")
ReadFile = File.read()
ListFile = list(ReadFile)
File_Size = len(ListFile)
Gen_Num = 0
Generations = Split_File(ListFile)

for i in range(len(Generations)):
    Generations[i] = Split_Generation(Generations[i])                           # Convert the list from [[Gen 1],[Gen2]] to [[[Gen 1 Symbol 1],...],[[Gen 2 Symbol 1],...]]

# --------------------------------------------------------------------------------------------------------------------

# File is not split into a workable list, list containing generations, which contain symbols (Read that later, have no idea what it means xD)

# First send a generation multiplied with an identity matrix
def Send_Raw_Packets():
    Raw_Packets_Sent = 0
    for i in range(len(Generations[Gen_Num])):
    #while Raw_Packets_Sent < len(Generations[Gen_Num]):
        Raw_Enc_Vec = []
        for j in range(len(Generations[Gen_Num])):                                  # Create an encoding vector with only one pivot element
            if j == Raw_Packets_Sent:
                Raw_Enc_Vec.append(1)
            else:
                Raw_Enc_Vec.append(0)
        Packet = Get_Enc_Packet_Pre_Defined_Enc_Vec(Generations[Gen_Num], Raw_Enc_Vec, File_Size, Gen_Num)
        base64_bytes = base64.b64encode(bytearray(Packet))
        base64_message = base64_bytes.decode('ascii')
        body['deviceQueueItem']['data'] = base64_message                            # File needs to be in a base64 ascii string format to be sent through chirpstack
        r = requests.post(d_queue_url, data=json.dumps(body), headers=headers)
        print("Raw packet " + str(Raw_Packets_Sent) + " Sent")
        print(Packet)
        Raw_Packets_Sent += 1
        #time.sleep(0.6)                                                             # Sleep 0.2 second to simulate bitrate of 250 bytes per second

# Second sends a generation multiplied by a random encoding vector
def Send_Encoded_Packets():
    Gen_Decoded = 0
    Packets_Sent = 0
    global Gen_Num
    while Gen_Decoded == 0:
        Packet = Get_Enc_Packet(Generations[Gen_Num], File_Size, Gen_Num)
        base64_bytes = base64.b64encode(bytearray(Packet))
        base64_message = base64_bytes.decode('ascii')
        body['deviceQueueItem']['data'] = base64_message                            # File needs to be in a base64 ascii string format to be sent through chirpstack
        r = requests.post(d_queue_url, data=json.dumps(body), headers=headers)
        print("Random packet " + str(Packets_Sent) + " Sent")
        print(Packet)
        # Find out how to receive packets, else make it on a timer
        # Received_Message = Whatever function is used to receive message from lopy
        # if Received_Message == b'Generation_Done':
        #    Gen_Num += 1
        #    Gen_Decoded = 1
        #time.sleep(0.6)                                                             # Sleep 0.2 second to simulate bitrate of 250 bytes per second

        # Code under here is to send a certain number of packets before stopping
        Packets_To_Send = 100
        Packets_Sent += 1
        if Packets_Sent == Packets_To_Send:
            Gen_Num += 1
            Gen_Decoded = 1


# ------------------------------------------The command list to send file-------------------------------------------
Update_File_Sending = 0
requests.delete(d_queue_flush_url, headers=headers)
print("Queue flushed")
time.sleep(1)
while Update_File_Sending == 0:
    Send_Raw_Packets()
    Send_Encoded_Packets()
    print("Generation " + str(Gen_Num) + " Sent")
    # Here make a function to stop updating if it receives the update done message from the lopy
    # Or if the lopy has sent a message saying the last generation has been decoded
    if Gen_Num == len(Generations):
        Update_File_Sending = 1
# ------------------------------------------------------------------------------------------------------------------

"""
Test_Packet = [2, 65, 233, 94, 32, 40, 29, 154, 179, 131, 149, 237, 97, 184, 243, 247, 135, 64, 91, 216, 166, 53, 64, 147, 171, 25, 11, 60, 106, 143, 226, 36, 142, 121, 231, 110, 85, 242, 163, 155, 49, 141, 173, 8, 115, 228, 216, 165, 57, 106]
Test_Packet2 = [2, 65, 233, 114, 19, 40, 5, 16, 146, 33, 242, 75, 250, 250, 94, 233, 84, 29, 143, 33, 82, 196, 112, 23, 8, 125, 224, 56, 63, 230, 145, 140, 123, 53, 158, 8, 146, 157, 89, 62, 245, 246, 228, 11, 225, 227, 81, 85, 230]

Packet_Bytearray = bytearray(Generations[0][0])
print(Packet_Bytearray)
"""

"""
#A byte type object can be converted to a list, and is in the desired format
Packet_Byte = bytes(Generations[0][0])
print(Packet_Byte)
Packet_List = list(Packet_Byte)
print(Packet_List)
for i in range(len(Packet_List)):
    if Packet_List[i] == Generations[0][0][i]:
        equal = 1
    else:
        equal = 0
        break
if equal:
    print("Equal")
else:
    print("Not equal")
"""

"""                                     # This converts a bytearray into a string array. This is not needed, as base64 can work with bytearrays
packet_bits = []

for i in Packet_Bytearray:
    b = bin(i)[2:].zfill(8)
    packet_bits.append(b)

print(packet_bits)
"""
"""
base64_bytes = base64.b64encode(Packet_Bytearray)
print(base64_bytes)
base64_message = base64_bytes.decode('ascii')
print(base64_message)

print(len(Packet_Bytearray))
print(len(base64_bytes))
print(len(base64_message))

# I need to make a function that encodes and sends the packets accordingly, while exchanging info with the sensor
"""
