from threading import *
from time import *
from socket import *
serverName = gethostname() #gets the Host name

Qtime = 10
TCPPort = 3256
UDPPort = 6123

last_input = None
def reader():
    global last_input
    while True: 
        last_input = input()  # always waits for next input


def input_with_timeout(prompt, timeout):
    print(prompt, end="", flush=True)
    global last_input
    start = time()
    old_value = last_input
    while time() - start < timeout:
        if last_input != old_value:  # new input arrived
            return last_input
        sleep(0.1)
    return "-"


TCPSocket=socket()# initalize a TCP Socket
TCPSocket.connect((serverName, TCPPort)) # connect to the host from the defined TCP port
UDPSocket=socket(AF_INET, SOCK_DGRAM)# Initalize UDP Socket, No Connection needed
#Phase 1: Joining the game
while True:
    data=TCPSocket.recv(1024).decode() #message is decoded after being recived
    if data.startswith("no replay"):
        break
    elif data.startswith("Game has already started"):# exit the client and close TCP Connection
        print(data)
        #TCPSocket.close()
        #UDPSocket.close()
        exit(1)
while True:
    client_name=input("Enter Your Name:\n")
    TCPSocket.send(f"JOIN {client_name}".encode()) # send client name and encode it
    userNameState=TCPSocket.recv(1024).decode()
    print(userNameState)
    if userNameState.startswith("Joining with username:"):# if any other thing just print the message and continue in the loop
        break
#Phase 2: Answering the questions
gameRules=TCPSocket.recv(1024).decode()
print(gameRules)
Thread(target=reader, daemon=True).start()
while True:
    questionInfo=TCPSocket.recv(1024).decode()# Question sent by TCP
    print(questionInfo, flush=True)
    if questionInfo.startswith("Final Results:"):
        break
    # tell the user to enter his answer in some specified time, if not enterd in this time "-" will be sent as wrong answer identification
    x = input_with_timeout("Enter your answer: ", Qtime)
    last_input="-"
    if x == "":
        x = "-"
    if x=="-":
        print()
    UDPSocket.sendto(f"{client_name}: {x}".encode(), (serverName, UDPPort))# Send it by UDP for faster transfer and reciption
    answerCorrectnes, serverAddress = UDPSocket.recvfrom(2048)# get the answer correctnes from the server
    answerCorrectnes=answerCorrectnes.decode()
    print(answerCorrectnes,flush=True)

#phase 3: Results
TCPSocket.close()# close TCP connection
UDPSocket.close()# close UDP connection