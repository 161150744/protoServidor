import os, sys, getopt
import socket
import threading
import logging
import hmac
import hashlib

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(threadName)s:%(message)s')

import request_pb2 as request
import response_pb2 as response
import communication
from pathlib import Path
from communication import (
    send_message, recv_message
)

def clientHMAC(request):
    data = requestcommand + requestpVersion + requesturl + requestcId + requestcInfo + requestencoding + requestcontent
    return str(hmac.new(b'passwd', data).hexdigest())

def serverHMAC(request):
    data = signature = response.status + response.pVersion + response.url + response.sInfo + response.encoding + response.content + response.signature
    return str(hmac.new(b'passwd', data).hexdigest())

def connect(connection, address):
    while 1:
        #request = receiveRequest(connection, request.Request())
        pass
        #if request:
         #   signature = hmac.new(b'passwd', signature)
          #  if signature == request:
           #     pass

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
        break
    return message

def createServer(IP, PORT):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((IP, int(PORT))) 
            sock.listen(10)
        except:
            logging.info("Fail to open server")
        logging.info("Server open in {0}".format(PORT))
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