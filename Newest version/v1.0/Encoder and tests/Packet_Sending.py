import requests
import json
import base64
import time
from File_Splitting import *
from Encode_Symbol import Encode_Symbol
from Random_Matrix import Random_1D_Bit_Matrix

# This is the program that sends a file to the LoPy and is the one used in the test to check the readability of the sent file

# Function that creates a random coefficients vector and encodes a generation with it
def Get_Enc_Packet(Generation, File_Size, Gen_Num, density = 0.2):                      # Arguments(Generation to encode, File size for header, Generation number for header, Density of random vector(Optional))
    Enc_Vec = Random_1D_Bit_Matrix(len(Generation), density)                            # Get the random coefficients vector
    while Enc_Vec == -1:                                                                # If the coefficients vector is empty
        Enc_Vec = Random_1D_Bit_Matrix(len(Generation), density)                        # Try and get another random vector
    Enc_Pack = Encode_Symbol(Generation, Enc_Vec, File_Size, Gen_Num)                   # Encode the generation with the random vector
    return Enc_Pack                                                                     # Return the encoded packet

def Get_Enc_Packet_Pre_Defined_Enc_Vec(Generation, Enc_Vec, File_Size, Gen_Num):        # Arguments(Generation to encode, Coefficients vector to encode with, File size for header, Generation number for header)
    Enc_Pack = Encode_Symbol(Generation, Enc_Vec, File_Size, Gen_Num)                   # Encode the generation with the given coefficients vector
    return Enc_Pack                                                                     # Return the encoded packet

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

# ------------------------------------------------Make Generation list globally---------------------------------------

File = open("Purple_Light.py","rb+")                                                    # Open the file to send
ReadFile = File.read()                                                                  # Read the file
ListFile = list(ReadFile)                                                               # Make a list of the file's data
File_Size = len(ListFile)                                                               # Read the file size in bytes
Gen_Num = 0
Generations = Split_File(ListFile)                                                      # Split the file into generations

for i in range(len(Generations)):
    Generations[i] = Split_Generation(Generations[i])                                   # Split the generations into symbols. Converts the list from [[Gen 1],[Gen2]] to [[[Gen 1 Symbol 1],...],[[Gen 2 Symbol 1],...]]

# --------------------------------------------------------------------------------------------------------------------

# Function to send uncoded symbols, by using a row of the identity matrix as coefficient vector
def Send_Raw_Packets():
    Raw_Packets_Sent = 0                                                                # Counter for the number of raw packets sent (Packets with uncoded symbols)
    for i in range(len(Generations[Gen_Num])):                                          # For the number of symbols in the generation
        for j in range(1):                                                              # Specifies how many times the packets are to be sent
            Raw_Enc_Vec = []                                                            # List to be filled with a row of the identity matrix
            for j in range(len(Generations[Gen_Num])):                                  # Create an encoding vector with only one 1 element
                if j == Raw_Packets_Sent:                                               # If this is the position to be filled with 1
                    Raw_Enc_Vec.append(1)                                               # Append 1
                else:                                                                   # Otherwise everwhere else
                    Raw_Enc_Vec.append(0)                                               # Append 0
            Packet = Get_Enc_Packet_Pre_Defined_Enc_Vec(Generations[Gen_Num], Raw_Enc_Vec, File_Size, Gen_Num)      # Create encoded packet with the identity vector
            base64_bytes = base64.b64encode(bytearray(Packet))                          # Encode packet in Base64
            base64_message = base64_bytes.decode('ascii')                               # Encode the Base64 packet in Ascii
            body['deviceQueueItem']['data'] = base64_message                            # Set the Base64 Ascii string as the data to be sent
            r = requests.post(d_queue_url, data=json.dumps(body), headers=headers)      # Send a post request to send the packet
            print("Raw packet " + str(Raw_Packets_Sent) + " Sent")                      # Print a feedback message
            print(Packet)                                                               # Print the packet that was sent
        Raw_Packets_Sent += 1                                                           # Increase the counter of sent packets by one

# Then sends a generation multiplied by a random encoding vector
def Send_Encoded_Packets():
    Gen_Decoded = 0                                                                     # Status of the generation decoding
    Packets_Sent = 0                                                                    # Counter for amount of encoded packets sent
    global Gen_Num                                                                      # Get the global generation number in order to increase it later
    while Gen_Decoded == 0:                                                             # While not all packets have been send
        Packet = Get_Enc_Packet(Generations[Gen_Num], File_Size, Gen_Num)               # Get an encoded packet, where the generation is encoded with a random coefficients vector
        base64_bytes = base64.b64encode(bytearray(Packet))                              # Encode packet in Base64
        base64_message = base64_bytes.decode('ascii')                                   # Encode the Base64 packet in Ascii
        body['deviceQueueItem']['data'] = base64_message                                # Set the Base64 Ascii string as the data to be sent
        r = requests.post(d_queue_url, data=json.dumps(body), headers=headers)          # Send a post request to send the packet
        print("Random packet " + str(Packets_Sent) + " Sent")                           # Print a feedback message
        print(Packet)                                                                   # Print the packet that was sent

        # Code under here is to send a certain number of packets before stopping
        Packets_To_Send = 100                                                           # Specify the number of packets to be sent
        Packets_Sent += 1                                                               # Increase the counter of sent packets by one
        if Packets_Sent == Packets_To_Send:                                             # Check if enough packets were sent
            Gen_Num += 1                                                                # Increase the generation number to start sending the next generation
            Gen_Decoded = 1                                                             # Declare the generation as decoded to stop the loop


# ------------------------------------------The command list to send file-------------------------------------------
Update_File_Sending = 0                                                                 # Status of the update
requests.delete(d_queue_flush_url, headers=headers)                                     # Send a request to flush the downlink queue
print("Queue flushed")                                                                  # Print a feedback message
time.sleep(1)                                                                           # Wait a second, so it is possible to flush the queue without sending packets
while Update_File_Sending == 0:                                                         # While not all packets have been sent
    Send_Raw_Packets()                                                                  # First send uncoded symbols
    Send_Encoded_Packets()                                                              # Then send coded symbols
    print("Generation " + str(Gen_Num) + " Sent")                                       # Print that the generation has been sent
    if Gen_Num == len(Generations):                                                     # Check if all packets have been sent
        Update_File_Sending = 1                                                         # Stop the update loop
# ------------------------------------------------------------------------------------------------------------------
