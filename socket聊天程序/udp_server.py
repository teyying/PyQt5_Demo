from socket import *

def main():
    udpSocket = socket(AF_INET, SOCK_DGRAM)
    # udpSocket = socket(AF_INET, SOCK_STREAM)
    udpSocket.bind(("", 5555))

    print("运行中")

    # 收， 打印
    while True:
        recvInfo = udpSocket.recvfrom(1024)
        print(f"{recvInfo[1]}:{recvInfo[0].decode()}")

if __name__ == '__main__':
    main()


