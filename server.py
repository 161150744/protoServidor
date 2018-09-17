import socket, os, sys
import request_pb2.py as request
import response_pb2.py as response
from communication import (
    send_message, recv_message
)


def sendRequest(sock, request):
    data = request.SerializeToString()
    size = encodeVarint(len(data))
    sock.sendall(size + data)

def receiveRequest(sock, protoType):
    data = b''
    while True:
        try:
            data += sock.recv(1)
            size = decodeVarint(data)
            break
        except IndexError:
            pass
    data = sock.recv(size)
    message = protoType()
    message.ParseFromString(data)

    return message

def createServer(IP, PORT):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(IP, PORT)
            sock.listen(1)
        except:
            logging.info("Erro ao abrir o servidor")
        logging.info("Servidor aberto na prota {0}".format(PORT))
        while True:
            connection, address = sock.accept()
            threading.Thread(target=connect, args=(connection, address)).start()
        sock.close()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Servidor finalizado")
        pass
            
def main(argv):
    criaConec(argv)

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print("Usage: {0} <Ip> <Port>".format(sys.argv[0]))
        exit(1)
    main(sys.argv[1:])