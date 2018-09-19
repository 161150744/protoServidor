import os, sys, getopt
import socket
import threading
import logging
import hmac
import hashlib

#Não sei pra que serve isso direito
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(threadName)s:%(message)s')

import request_pb2 as request
import response_pb2 as response

#Tira o HMAC do cliente
def clientHMAC(request):
    data = requestcommand + requestpVersion + requesturl + requestcId + requestcInfo + requestencoding + requestcontent
    return str(hmac.new(b'passwd', data).hexdigest())
#Tira o HMAC do server
def serverHMAC(request):
    data = signature = response.status + response.pVersion + response.url + response.sInfo + response.encoding + response.content + response.signature
    return str(hmac.new(b'passwd', data).hexdigest())   

#Função que se conecta
def connect(connection, address):
    while 1:
        request = receiveRequest(connection, request.Request())
       
        signature = hmac.new(b'passwd', signature)
        if signature == request.signature:
            if request.command == "DELETE":
                #response = chamaFunDel()
                sendRequest(connection, response)
            else if request.command == "GET":
                #response = chamaFunGet()
                sendRequest(connection, response)
            else if request.command == "POST":
                #response = chamaFunPost()
                sendRequest(connection, response)
            else:
                #funError()
    connection.close()

def sendRequest(sock, request):
    data = request.SerializeToString()
    size = struct.pack('>L', len(data))
    sock.sendall(size + data)

def receiveRequest(sock, request):
    while 1:
        print("Listening...")
        buf_len = sock.recv(4)
        msg_len = struct.unpack('>L', buf_len)[0]
        msg_buf = sock.recv(msg_len)
        message = request()
        message.ParseFromString(msg_buf)
        print (message)
        
    return message

#Função que cria o server
def createServer(IP, PORT):
    #Cria um socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Vincula o socket a um endereço
        try:
            sock.bind((IP, int(PORT))) 
            sock.listen(10)
        except:
            logging.info("Fail to open server")
        logging.info("Server open in {0}".format(PORT))
        #Chama a função que contém as opções de requisição
        while 1:
            connection, address = sock.accept()
            threading.Thread(target=connect, args=(connection, address)).start()
        sock.close()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Server closed")
        pass
            
def main(argv):
    IP, PORT = argv
    createServer(IP, PORT)

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print("Usage: {0} <Ip> <Port>".format(sys.argv[0]))
        exit(1)
    main(sys.argv[1:])