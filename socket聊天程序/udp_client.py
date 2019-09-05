from socket import *

udpSocket = socket(AF_INET, SOCK_DGRAM)
# udpSocket = socket(AF_INET, SOCK_STREAM)
udpSocket.sendto('liupeng44你好'.encode(), ("192.168.31.112", 6789))
udpSocket.sendto('liupeng44你好'.encode(), ("192.168.31.112", 5555))
udpSocket.sendto('liupeng44你好'.encode(), ("192.168.31.113", 69))
