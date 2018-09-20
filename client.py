import os, sys, getopt
import socket
import random
import request_pb2 as request
import response_pb2 as response
import server
import struct

def help():
	print("Options:")
	print("GET - Get something from the server")
	print("POST - Send something to the server")
	print("DELETE - Delete something from the server")
	print("EXIT - Close connection")
	print("OBS: The commands are not case sensitive. \n")

def isAvailable(command):
	lista = ["GET", "POST", "DELETE", "EXIT"]

	for i in lista:
		if i == command:
			return True
	print("\n\nINVALID COMMAND!\nTRY AGAIN:")
	help()
	return False

def createConnection(IP, PORT):
	#Cria o socket e tenta conectar
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((IP, int(PORT)))
		print("Connection successfully established!")
	except ConnectionRefusedError:
		print("Could not connect! Exiting...")
		exit(1)
	help() #Mostra funções disponíveis
	#Pega o comando do usuário
	command = ""
	clientId = str(random.randint(1000,9999))
	while(command != "EXIT"):
		command = command = input("Type your command:").upper()
		if(command == "EXIT"):
			break
		if(not isAvailable(command)):
			command = ""
			continue
		req = request.Request()
		req.command = command
		req.url = input("URL: ")
		req.cId = clientId
		print(req.cId)
		req.pVersion="Version: 1.0"
		req.cInfo="Version: 1.0"
		req.encoding="utf-8"
		#Se for GET ou DELETE, não tem conteúdo na requisição
		if((req.command == "GET") or (req.command == "DELETE")):
			req.content = ""
		else: #Se for post, busca o arquivo e coloca o seu conteúdo na requisição
			if(os.path.exists("{0}".format(req.url))):
				file = open("{0}".format(req.url), 'r')
				req.content = file.read()
				file.close()
		#Faz o HMAC da requisição
		req.signature = server.clientHMAC(req)
		#Envia a requisição
		server.sendRequest(sock, req)
		#Pega a resposta do servidor
		resp = server.receiveRequest(sock, response.Response)
	
		#Faz HMAC do servidor
		signature = server.serverHMAC(resp)
		#Se for igual, houve resposta então mostra resultado
		if signature == resp.signature:
			print("\n Server response")
			if req.command.upper() == "GET":
				print("Status:", resp.status)
				if("OK" in resp.status):
					print("Content:")
					print(resp.content)
				else:
					print("File not found")
			elif req.command.upper() == "POST":
				print("Status:", resp.status)
				if("OK" in resp.status):
					print("File {0} was created!".format(resp.url))
				else:
					print("Error creating file!")
			elif req.command.upper() == "DELETE":
				print("Status:", resp.status)
				if("OK" in resp.status):
					print("File {0} was successful deleated!")
				else:
					print("Error deleting file!")
			else:
				#print("Status:", resp.status)
				print("Command not found!")
		#Ao final, mostra as opções para fazer uma nova requisição
		print(" \n_______New Request_______")
		help()

def main(argv):
    IP, PORT = argv
    createConnection(IP, PORT)

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print("Usage: {0} <Ip> <Port>".format(sys.argv[0]))
        exit(1)
    main(sys.argv[1:])