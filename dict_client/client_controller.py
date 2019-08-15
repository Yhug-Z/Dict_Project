"""
    tcp 客户端链接
"""
from socket import socket

class ClientController:
    def __init__(self, ip="127.0.0.1",port=21608):
        self.__ip=ip
        self.__port=port
        self.__addr=(self.__ip,self.__port)
        self.__create_sorket()

    def __create_sorket(self):
        self.__sorkfd=socket()

    def run(self):
        self.__sorkfd.connect(self.__addr)
        while True:
            data=self.__sorkfd.recv(1024)
            print(data.decode())
            command=input("")
            self.__sorkfd.send(command.encode())
            if command=="3":
                break

#=====================================
if __name__ == '__main__':
    client=ClientController(port=21609)
    client.run()