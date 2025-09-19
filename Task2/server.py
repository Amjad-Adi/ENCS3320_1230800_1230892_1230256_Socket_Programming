import os
from socket import *
from threading import *
from time import *
from random import *

gameStarted = False
quesFlag=False
finishFlag=False
minPlayers = 2
maxPlayers = 4
playerList = []
scoreList = []
# playerList and scoreList are parallel Lists
Qtime = 10
timeToStart = 30
n = 5
Qnum = 1
seq = []
QList = []
quesFlag = True
nextQ = False
dir = os.path.dirname(__file__)# get this server.py directory path
quesFile = os.path.join(dir, 'Questions.txt')# access the Questions.txt file
numberOfAnswers=0# to count the number of answers recived for each question
finishedClients=0# number of finished client threads

#id=1230256, port = (last 3 digits) + 3000 = 3256
TCPPort = 3256 
TCPSocket = socket(AF_INET,SOCK_STREAM)# intialize TCP socket to collect streams of bits
TCPSocket.bind(('',TCPPort))# collect every TCP msg sent into TCPPort
TCPSocket.listen(4)

#id=1230256, port = (first 3 digits) + 6000 = 6123
UDPPort = 6123
UDPSocket = socket(AF_INET,SOCK_DGRAM)# intialize UDP socket to collect msgs
UDPSocket.bind(('',UDPPort))# collect every UDP msg sent into UDPPort

print ('The server is ready to receive')

def generateQuesSequence (count) :# to generate a random sequence of questions from 1 to count
    numbers = []
    for i in range (0,count):
        numbers.append(i)
    shuffle(numbers) 
    return numbers

def quesList():#return a list of list contaning each question and its answer
    questionList=[]
    try:
        f=open(quesFile,"r")
    except:
        print("There is no \"Questions.txt\" file")
        exit()
    fileInfo=f.read()#read all questions to split them
    quesInfo=fileInfo.split("\n$\n")# split based on question
    for question in quesInfo:
        questionList.append(question.split("\n#\n"))# split based on QuestionInfo, Answer
    return questionList

def checkAnswers(questions,order,clientAnswer) :#check if the question is answered correctly and return a true if it is flase if not
    correctAnswer = questions[order][-1].strip()
    return correctAnswer.lower() == clientAnswer.lower()

def handle_client(client_socket: socket, addr):
    quesFlag = True
    while True:
        data = client_socket.recv(2048).decode()
        if data.startswith("JOIN "):
            username = data[5:].strip()
            if not gameStarted:
                if username not in playerList:
                    playerList.append(username) #adding player to the player list
                    scoreList.append(0) #add a score element to the player with initial score 0.
                    client_socket.send(b"Joining with username: " + username.encode()+b"\n")
                    break
                else:
                    client_socket.send(b"This username is already taken. Try another one.\n")
            else:
                client_socket.send(b"Game has already started. Please wait for the next round.\n")
        else:
            client_socket.send(b"Invalid command. Use JOIN <username> to join the game.\n")
    while not gameStarted:
        pass
    client_socket.send(f"Game will start soon, be ready for it\nGame rules:\n1. There's {n} questions.\n2. You have {Qtime} seconds to answer each question.\n3. Correct answer gives you 1 point, wrong answer 0 points.\n4. No use of external help allowed.\n5. Have fun!\n\n".encode())
    sleep(0.5)
    while True:
        global Qnum
        if Qnum > n:# if sent questions is more than the questions, the game ends
            s="Final Results:\n"
            for i in range(len(playerList)):# send Result msg
                s += f"{playerList[i]}: {scoreList[i]} point{"s" if scoreList[i] != 1 else ""}\n"
            maxScore = scoreList.index(max(scoreList))
            s+= f"Winner: {playerList[maxScore]}\n"# the player with max score (The Winner)
            client_socket.send(s.encode())
            global finishedClients
            finishedClients+=1
            global finishFlag
            finishFlag = True
            break
        elif quesFlag:
            quesFlag = False
            client_socket.send(f"Q{Qnum}: {QList[Qnum-1][0]}".encode()) #send question to client
            #sleep(Qtime)
        global numberOfAnswers
        global nextQ
        if nextQ:
            quesFlag = True
            numberOfAnswers -= 1 # set numOfAnswers=0 for next question
            if numberOfAnswers == 0:
                nextQ = False
    client_socket.close()# close client TCP connection

def timer_thread():
    sleep(timeToStart)
    global gameStarted
    while len(playerList) < minPlayers: 
        pass
    gameStarted = True

def accept_clients():
    while True:
        connectionSocket, addr = TCPSocket.accept()
        if len(playerList) < maxPlayers:
            connectionSocket.send(b"no replay")
            client = Thread(target=handle_client, args=(connectionSocket, addr)) #creating a thread for each client TCP connection
            client.start() #starting the thread
        else:
            connectionSocket.send(b"Game is full. Try again later.")
            connectionSocket.close()#if num of players is max close next client connection

QList = quesList()# take the question, answer list of list
seq = generateQuesSequence(n)# generate the random sequece for 5 questions
Thread(target=timer_thread).start()#thread running parallel to the while loops waiting till all players enter
accept_client = Thread(target=accept_clients)#thread to accept clients
accept_client.daemon = True
accept_client.start()# start the thread to accept clients
print(seq)
for i in seq:
    print(QList[i][-1].strip())
while True:
    if gameStarted and Qnum<=n:
        message, clientAddress = UDPSocket.recvfrom(1024)# recive msg and the client whoo sent it address
        message = message.decode()
        print(message)# display client message in terminal
        numberOfAnswers += 1
        playername = message.strip().split(" ")[0][:-1]#take playername
        ans = message.strip().split(" ")[-1]#take answer
        if checkAnswers(QList, seq[Qnum-1], ans):# check the answer if it is correct
            UDPSocket.sendto(b"Correct\n", clientAddress)# if corect then send that it is correct to that client
            scoreList[playerList.index(f"{playername}")] += 1# increase his score by 1
        else:
            UDPSocket.sendto(b"Wrong\n", clientAddress)# else send wrong
        if numberOfAnswers == len(playerList): # check if all players answered the question, to go to the second question
            nextQ = True# set nextQ to True to allow sending the next question
            Qnum += 1# increase num of questions by 1 to stop when equals intended numOfQuestions
    elif finishedClients == len(playerList) and finishFlag:
        TCPSocket.close()# close server TCP connection and socket
        UDPSocket.close()#close server UDP Socket
        break
