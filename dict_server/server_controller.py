"""
    tcp 服务器  协程 并发
"""
from gevent import monkey

from dict_server.dict_controller import DictController

monkey.patch_socket()

from socket import *
import gevent

class ServerController:
    def __init__(self, ip="0.0.0.0", port=21608):
        self.__ip = ip
        self.__port = port
        self.__addr = (self.__ip, self.__port)
        self.__create_socket()
        self.__bind()

    def __create_socket(self):
        self.__sockfd = socket()
        self.__sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def __bind(self):
        self.__sockfd.bind(self.__addr)
        self.__sockfd.listen(5)

    def run(self):
        while True:
            connfd,addr=self.__sockfd.accept()
            print("Connect from:",addr)
            gevent.spawn(DictController().run,connfd,addr)


#===========================
if __name__ == '__main__':
    server=ServerController(port=21609)
    server.run()