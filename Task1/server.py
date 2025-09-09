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
	#print(userInput)
	if userInput and userInput.startswith('GET '):
		userInput = userInput.split(' ')
		if userInput and len(userInput) >= 2 and userInput[1].startswith('/'):
			userInput = userInput[1]
			flag = False
			dirToRead=""
			if userInput == "/" or userInput == "/index.html" or userInput == "/en" or userInput == "/main_en.html":
				userInput = "main_en.html"
				dirToRead=task1_dir
				if "main_en.html" in os.listdir(dirToRead):
					phrase = "200 OK"
				else:
					phrase = "404 Not Found"
			elif userInput == "/ar" or userInput == "/main_ar.html":
				userInput = "main_ar.html"
				dirToRead=task1_dir
				if "main_ar.html" in os.listdir(dirToRead):
					phrase = "200 OK"
				else:
					phrase = "404 Not Found"
			elif userInput.startswith("/?filename="):
				flag = True
				dirToRead=available_dir
				userInput = userInput[11:]
				if not os.path.exists(dirToRead):
					phrase = "404 Not Found"
				else:
					if userInput in os.listdir(dirToRead):
						if "private" in userInput:
							phrase = "403 Forbidden"
						else:
							phrase = "200 OK"
					else:
						phrase = "404 Not Found"
			else:
				flag = True
				userInput = userInput[1:]
				dirToRead=task1_dir
				if userInput in os.listdir(dirToRead):
					if "private" in userInput:
						phrase = "403 Forbidden"
					else:
						phrase = "200 OK"
				else:
					phrase = "404 Not Found"
		else:
			userInput = userInput[1]
			phrase = "404 Not Found"
	else:
		userInput = "Null"
		phrase = "403 Forbidden"
	
	print("IP: " + addr[0] + ", Port: " + str(addr[1]))
	print("Requested resource: " + userInput)
	print("Status code: " + phrase.split(" ")[0] + "\n\n")

	s=f"HTTP/1.1 {phrase}\r\n"

	if phrase == "404 Not Found": userInput = "error404.html"
	elif phrase == "403 Forbidden": userInput = "error403.html"

	if phrase == "200 OK":
		if flag:
			if userInput.endswith(".css"):
				s+='Content-Type: text/css\r\n'
			else:
				s+='Content-Type: application/octet-stream\r\n'
				s+=f'Content-Disposition: filename="{userInput}"\r\n'

			f = open(os.path.join(dirToRead, userInput), 'rb')
			data = f.read()
			s+=f'Content-Length: {len(data)}\r\n'
		else:
			s+='Content-Type: text/html \r\n'
			f = open(os.path.join(dirToRead, userInput), 'rb')
			data = f.read()
	else:
		s+='Content-Type: text/html \r\n'
		f = open(os.path.join(task1_dir, userInput), 'r')
		data = f.read().format(f"IP: {addr[0]}, Port: {addr[1]}").encode()
	s+='\r\n'
	# print(s)
	# print(data)
	connectionSocket.send(s.encode())
	connectionSocket.send(data)
	connectionSocket.close()
