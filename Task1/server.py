import os
from socket import *
task1_dir = os.path.dirname(__file__)
available_dir = os.path.join(task1_dir, 'Available Files\\')
port = 5256
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', port))
serverSocket.listen(1)
print("The server is ready to receive")
while True:
	connectionSocket, addr = serverSocket.accept()
	userInput = str(connectionSocket.recv(1024).decode())
	if not userInput or "filename=" not in userInput:
		connectionSocket.close()
		continue
	print(userInput)
	userInput = userInput.split(' ')[1][11:]
	if userInput and userInput.startswith('%2F'):
		userInput = userInput[3:]
	print("IP: " + addr[0] + ", Port: " + str(addr[1]))
	print("Requested resource: " + userInput)
	if not os.path.exists(available_dir):
		phrase = "404 Not Found"
	else:
		flag = False
		if userInput == "" or userInput == "index.html" or userInput == "en" or userInput == "main_en.html":
			userInput = "main_en.html"
			if "main_en.html" in os.listdir(task1_dir):
				phrase = "200 OK"
			else:
				phrase = "404 Not Found"
		elif userInput == "ar" or userInput == "main_ar.html":
			userInput = "main_ar.html"
			if "main_ar.html" in os.listdir(task1_dir):
				phrase = "200 OK"
			else:
				phrase = "404 Not Found"
		else:
			flag = True
			if userInput in os.listdir(available_dir):
				if "private" in userInput:
					phrase = "403 Forbidden"
				else:
					phrase = "200 OK"
			else:
				phrase = "404 Not Found"
	print("Status code: " + phrase.split(" ")[0] + "\n\n\n")
	s=f"HTTP/1.1 {phrase}\r\n"
	if phrase == "404 Not Found": userInput = "error404.html"
	elif phrase == "403 Forbidden": userInput = "error403.html"
	if phrase == "200 OK":
		if flag:
			s+='Content-Type: application/octet-stream\r\n'
			s+=f'Content-Disposition: filename="{userInput}"\r\n'
			f = open(os.path.join(available_dir, userInput), 'rb')
			data = f.read()
		else:
			s+='Content-Type: text/html \r\n'
			f = open(os.path.join(task1_dir, userInput), 'rb')
			data = f.read()
	else:
		s+='Content-Type: text/html \r\n'
		f = open(os.path.join(task1_dir, userInput), 'r')
		data = f.read().format(addr[0], addr[1]).encode()
	s+='\r\n'
	# print(s)
	connectionSocket.send(s.encode())
	connectionSocket.send(data)
	connectionSocket.close()
