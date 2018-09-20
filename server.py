import os, sys, getopt
import socket
import threading
import logging
import hmac
import hashlib
import struct

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(threadName)s:%(message)s')

import request_pb2 as request
import response_pb2 as response
import communication
from pathlib import Path
from communication import (
    send_message, recv_message
)

def clientHMAC(req):
    data = req.command + req.pVersion + req.url + req.cId + req.cInfo + req.encoding + req.content
    return str(hmac.new(b'passwd', data.encode("UTF-8")).hexdigest())

def serverHMAC(req):
    data = req.status + req.pVersion + req.url + req.sInfo + req.encoding + req.content
    return str(hmac.new(b'passwd', data.encode("UTF-8")).hexdigest())

def connect(connection, address):
    command = {"GET":GET, "POST":POST, "DELETE":DELETE}
    if not os.path.exists("./_Arq"):
        os.makedirs("_Arq")
    while 1:
        req = receiveRequest(connection, request.Request)
        if req:
            signature = clientHMAC(req)
            if signature == req.signature:
                res = command[req.command.upper()](req)
                res.signature = serverHMAC(res)
                sendRequest(connection, res)

def GET(req):
    res = response.Response()
    try:
        if req.url == "/":
            file = open("./_Arq/index.html")
        else:
            file = open("{0}/{1}".format("./_Arq/", req.url))
        res.content = file.read()
        file.close()
        logging.info("200 - OK - GET")
        res.status = "200 - OK"
    except:
        res.content = ""
        logging.info("404 - NOT FOUND")
        res.status = "404 - NOT FOUND"
    res.pVersion="Version: 1.0"
    res.url="{0}/{1}".format("./_Arq/", req.url)
    res.sInfo="Version: 1.0"
    res.encoding="utf-8"
    return res


def POST(req):
    res = response.Response()
    try:
        file = open("{0}/{1}".format("./_Arq", req.url.split('/')[len(req.url.split('/'))-1]), "w")
        file.write(req.content)
        file.close()
        file2 = open("{0}/.{1}.{2}".format("./_Arq", req.cId, req.url.split('/')[len(req.url.split('/'))-1]), "w")
        file2.write(".")
        file2.close()
        logging.info("200 - OK - POST")
        res.status = "OK"
    except:
        res.status = "ERROR"
        logging.info("200 - OK - GET")
    res.pVersion="Version: 1.0"
    res.url="{0}/{1}".format("./_Arq", req.url)
    res.sInfo="Version: 1.0"
    res.encoding="utf-8"
    res.content=req.content
    return res

def DELETE(req):
    res = response.Response()
    if(os.path.isfile("{0}/.{1}.{2}".format("./_Arq", req.cId, req.url))):
        os.remove("{0}/.{1}.{2}".format("./_Arq", req.cId, req.url))
        os.remove("{0}/{1}".format("./_Arq", req.url))
        res.status = "OK"
    else:
        res.status = "ERRO"
    res.pVersion="Version: 1.0"
    res.url="{0}/{1}".format("./_Arq", req.url)
    res.sInfo="Version: 1.0"
    res.encoding="utf-8"
    res.content=req.content
    return res

def sendRequest(sock, req):
    data = req.SerializeToString()
    size = struct.pack('>L', len(data))
    sock.sendall(size + data)

def receiveRequest(sock, req):

    len_buf = sock.recv(4)
    msg_len = struct.unpack('>L', len_buf)[0]
    msg_buf = sock.recv(msg_len)
    msg = req()
    msg.ParseFromString(msg_buf)
   # print(msg)
    return msg

def createServer(IP, PORT):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((IP, int(PORT))) 
            sock.listen(10)
            logging.info("Server open in {0}".format(PORT))
        except:
            logging.info("Fail to open server")
            exit(1)
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