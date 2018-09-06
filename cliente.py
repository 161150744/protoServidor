import socket, os, sys
import entropy_pb2 as data
from communication import (
    send_message, recv_message
)

def criaConec(argv):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((argv[0], int(argv[1])))
    
    message = data.Entropy()
    message.request = input("Digite a requisição => ") # get
    message.data = input("Digite os dados => ") # /
    send_message(sock, message)
    buffer = recv_message(sock)

    if buffer:
        pass


def main(argv):
    criaConec(argv)

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print("Usage: {0} <Ip> <Port>".format(sys.argv[0]))
        exit(1)
    main(sys.argv[1:])