import os
from socket import *
task1_dir = os.path.dirname(__file__)	# Directory of the server
available_dir = os.path.join(task1_dir, 'Server Database')	# Directory of available files
html_dir = os.path.join(task1_dir, 'HTML Files')			# Directory of HTML files
css_dir = os.path.join(task1_dir, 'CSS Files')				# Directory of CSS files

# Port number (5000 + last 3 digits of 1230256 = 5256)
port = 5256 
serverSocket = socket(AF_INET, SOCK_STREAM) # Create a TCP socket
serverSocket.bind(('', port))				# Bind the socket to server port
serverSocket.listen(1) 						# Enable the server to accept connections (max 1 connection)
print("The server is ready to receive")

flagLanguage = True # True for English, False for Arabic
# Server run loop
while True:
	connectionSocket, addr = serverSocket.accept() # Establish connection with client
	userInput = str(connectionSocket.recv(1024).decode()) # Read client request
	if userInput and userInput.startswith('GET '): # Check if the request is a GET request
		userInput = userInput.split(' ') # Split the request
		# Check if the request is valid (the size of the list is greater or equal to 2 and the second part starts with /)
		if userInput and len(userInput) >= 2 and userInput[1].startswith('/'):
			userInput = userInput[1] 	# Get the requested resource (file name)
			dirToRead="" 				# Directory to read the file from
			# Checking if the requested resource is for English (/, /index.html, /en, /main_en.html)
			if userInput == "/" or userInput == "/index.html" or userInput == "/en" or userInput == "/main_en.html":
				flagLanguage = True			# Set language to English
				userInput = "main_en.html"	# Set the file name to main_en.html
				dirToRead=html_dir			# Set the directory to read the file from
				# Check if the file exists in the directory and set the status code phrase
				if "main_en.html" in os.listdir(dirToRead): 
					phrase = "200 OK"
				else:
					phrase = "404 Not Found"
			# Checking if the requested resource is for Arabic (/ar, /main_ar.html)
			elif userInput == "/ar" or userInput == "/main_ar.html":
				flagLanguage = False			# Set language to Arabic
				userInput = "main_ar.html"		# Set the file name to main_ar.html
				dirToRead=html_dir				# Set the directory to read the file from
				# Check if the file exists in the directory and set the status code phrase
				if "main_ar.html" in os.listdir(dirToRead):
					phrase = "200 OK"
				else:
					phrase = "404 Not Found"
			# Checking if the requested resource is for a file in the Server Database (/?name=FILE_NAME)
			elif userInput.startswith("/?name="):
				dirToRead=available_dir		# Set the directory to read the file from
				userInput = userInput[7:]	# Get the file name from the request (by removing "/?name=")
				# Check if the directory exists, if not set the status code phrase to 404 Not Found
				if not os.path.exists(dirToRead):
					phrase = "404 Not Found"
				else:
					# Check if the file exists in the directory and set the status code phrase
					if userInput in os.listdir(dirToRead):
						if "private" in userInput:
							phrase = "403 Forbidden"
						else:
							phrase = "200 OK"
					else:
						phrase = "404 Not Found"
			# Checking if the requested resource is for other file types (.html, .css, .*)
			else:
				userInput = userInput[1:]	# Get the file name from the request (by removing "/")
				# Check if the requested file is .html or .css specifically, otherwise check in the database directory
				dirToRead=html_dir if userInput.endswith(".html") else css_dir if userInput.endswith(".css") else available_dir
				# Check if the directory exists, if not set the status code phrase to 404 Not Found
				if userInput in os.listdir(dirToRead):
					if "private" in userInput:
						phrase = "403 Forbidden"
					else:
						phrase = "200 OK"
				else:
					phrase = "404 Not Found"
		# If the request is not valid, set the status code phrase to 404 Not Found
		else:
			# Get the file name from the request (by removing "/")
			userInput = userInput[1:] if len(userInput) > 1 else "Null"
			phrase = "404 Not Found"
	# If the request is empty or not a GET request, set the status code phrase to 403 Forbidden
	else:
		userInput = "Null"
		phrase = "403 Forbidden"
	
	# Print the request details
	print("IP: " + addr[0] + ", Port: " + str(addr[1]))
	print("Requested resource: " + userInput)
	print("Status code: " + phrase.split(" ")[0] + "\n\n")

	# Send the response to the client
	s=f"HTTP/1.1 {phrase}\r\n"

	# If the phrase is 404 Not Found or 403 Forbidden, set the userInput to the corresponding HTML file
	if phrase == "404 Not Found": userInput = "404Error_en.html" if flagLanguage else "404Error_ar.html"
	elif phrase == "403 Forbidden": userInput = "403Error_en.html" if flagLanguage else "403Error_ar.html"

	# Set the content type and read the file data
	if phrase == "200 OK":
		# if the file is .css or .html, set the content type to text/css or text/html, otherwise set it to application/octet-stream
		if userInput.endswith(".css") or userInput.endswith(".html"):
			s+=f'Content-Type: text/{userInput.split(".")[1]}\r\n'
		else:
			s+='Content-Type: application/octet-stream\r\n'
		s+=f'Content-Disposition: filename="{userInput}"\r\n'

		f = open(os.path.join(dirToRead, userInput), 'rb')
		data = f.read()
		f.close()
	else:
		# For 404 and 403 errors, the content type is always text/html
		s+='Content-Type: text/html \r\n'
		f = open(os.path.join(html_dir, userInput), 'rb')
		data = f.read().decode().format(f"IP: {addr[0]}, Port: {addr[1]}").encode()
		f.close()

	s+='\r\n'
	connectionSocket.send(s.encode()) 	# Send the response header
	connectionSocket.send(data)			# Send the response body
	connectionSocket.close() 			# Close the connection socket


	