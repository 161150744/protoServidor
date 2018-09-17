import os, sys, getopt
import socket
import random
import request_pb2 as request
import response_pb2 as response
import communication	
import hashlib
import hmac
import server

def availableFuncHelp():
	print("Options:")
	print("GET - Get something from the server")
	print("POST - Send something to the server")
	print("DELETE - Delete something from the server")
	print("EXIT - Close connection")

def createConnection(IP, PORT):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect(IP, int(PORT))
		print("Connection successfully established!")
	except: ConnectionRefusedError:
		print("Could not connect! Exiting...")
		exit(1)

	request = request.Request()
	command = input("Type your command:").upper()
	availableFuncHelp()
	while(command != "EXIT")
		req = request.Request()
		req.command = command
		req.upper input("URL: ")
		req.cId = 3

		if((req.command == "GET") or (req.command == "DELETE"))
			message.content = ""
		else:
			if(os.path.exists(req.url)):
				file = open(req.url, 'r')
				req.content += file.read()
				file.close()

		signature = req.command + req.pVersion + req.url + req.cId + req.cInfo + req.encoding + req.content
		

		req.signature = hmac.new(b'passwd', signature)

		server.sendRequest(sock, req)

		resp = server.receiveResponse(sock, response.Response())
		
		if resp:
			signature = resp.status + resp.pVersion + resp.url + resp.sInfo + resp.encoding + resp.content + resp.signature

			if signature == resp.signature:
				print("\n Server response")
				if req.command == "GET":
					print("Status:", resp.status)
					if("OK" in resp.status)
						print("Content:")
						print(resp.content)
					else:
						print("File not found")
				elif req.command = "POST":
					print("Status:", resp.status)
					if("OK" in resp.status):
						print("File {0} was created!".format(resp.url))
					else:
						print("Error creating file!")
				elif req.comman == "DELETE":
					print("Status:", resp.status)
					if("OK" in resp.status):
						print("File {0} was successful deleated!")
					else:
						print("Error deleting file!")
				else:
					print("Status:", resp.status)
					print("Command not found!")
			print("_______New Request______")
			command = input("Type your command:").upper()