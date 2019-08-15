"""
    字典 控制器
"""
from dict_server.dir_model.user_model import UserModel
from dict_server.mysql_controller.user_controller import UserController
from dict_server.mysql_controller.words_controller import WordsController


class DictController:
    def __init__(self):
        self.__user_controller = UserController('dict', 'User')
        self.__words_controller= WordsController("dict","words")
        self.__globle_msg = ""

    def run(self, connfd, addr):
        self.__connfd = connfd
        self.__addr = addr
        self.__first_view()

    def __first_view(self):
        while True:
            self.__globle_msg += self.__menu_first() + "\nCommand:"
            try:
                self.__connfd.send(self.__globle_msg.encode())
            except OSError:
                print(self.__addr,"end")
                break
            command = self.__connfd.recv(1024).decode()
            if self.__handle_command(command):
                pass
            else:
                break

    def __menu_first(self):
        return """
                ============================
                1.登入       2.注册     3.退出
                ============================
        
                """

    def __login(self):
        msg = "登入...\n请输入用户名："
        self.__connfd.send(msg.encode())
        name = self.__connfd.recv(32).decode()
        msg = "\n请输入密码："
        self.__connfd.send(msg.encode())
        password = self.__connfd.recv(32).decode()
        result = self.__user_controller.login(name, password)
        if result:
            self.__second_view()
            return (True,)
        else:
            return (False, "Login Failure\n")

    def __second_view(self):
        self.__globle_msg=""
        while True:
            self.__globle_msg += self.__menu_second() + "\nCommand:"
            self.__connfd.send(self.__globle_msg.encode())
            command = self.__connfd.recv(1024).decode()
            if not command or command=="3":
                self.__connfd.close()
                break
            elif command == "4":
                break
            elif command=="1":
                self.__find_word()
            elif command=="2":
                pass
            else:
                self.__globle_msg = "Command Error\n"


    def __menu_second(self):
        return """
                ==================================
                1.查单词   2.历史记录  3.退出  4.注销
                ==================================

                """

    def __exit(self):
        self.__connfd.close()

    def __register(self):
        msg = "注册...\n请输入用户名："
        self.__connfd.send(msg.encode())
        name = self.__connfd.recv(32).decode()
        msg = "\n请输入密码："
        self.__connfd.send(msg.encode())
        password = self.__connfd.recv(32).decode()
        result = self.__user_controller.register(UserModel(name, password))
        if result[0]:
            msg = "Register Success\n"
            msg += "输入Y进入字典："
            self.__connfd.send(msg.encode())
            command = self.__connfd.recv(4).decode()
            if command == "Y":
                self.__second_view()
                self.__globle_msg = ""
        else:
            self.__globle_msg = result[1] + "\n"

    def __handle_command(self, command):
        if not command or command == "3":
            self.__exit()
            return False
        if command in '12':
            if command == "1":
                # print(command)
                result = self.__login()
                if result[0]:
                    self.__globle_msg = ""
                else:
                    self.__globle_msg = result[1]
            elif command == "2":
                self.__register()
        else:
            self.__globle_msg = "Command Error\n"

        return True

    def __find_word(self):
        msg="请输入单词："
        self.__connfd.send(msg.encode())
        word=self.__connfd.recv(1024).decode()
        mean=self.__words_controller.find(word)
        if mean:
            self.__globle_msg=mean+"\n"
        else:
            self.__globle_msg = "Can't find word" + "\n"
