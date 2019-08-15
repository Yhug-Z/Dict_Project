"""
    用户登入和注册控制器
"""
import pymysql


class UserController:
    """
       依据数据库mysql 用户登入和注册验证 控制器
    """

    def __init__(self, database, table, host='localhost', port=3306, user='root', password='123456',
                 charset='utf8'):
        self.db = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                                  charset=charset)
        self.cur = self.db.cursor()
        self.table = table

    def register(self, target):
        """
            注册 用户
        :param target:用户账号，密码数据模型
        :return: 成功返回(True,)，失败返回false及错误原因
        """
        if self.__is_exist_by_condition("name='%s'" % target.user_name):
            return (False, "User name exist.")
        try:
            self.cur.execute(self.__sql_insert(), [target.user_name, target.password])
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            return (False, str(e))
        return (True,)

    def login(self, name, passwd):
        """
            登入检测
        :param name: 用户名
        :param passwd: 用户密码
        :return: 用户密码正确返回True，不正确返回False
        """
        if self.__is_exist_by_condition("name='%s' and password='%s'" % (name, passwd)):
            return True
        else:
            return False

    def __is_exist_by_condition(self, condition):
        self.cur.execute(self.__sql_select(" where " + condition))
        if self.cur.fetchone():
            return True
        return False

    def __sql_select(self, condition=''):
        if condition:
            return "select * from " + self.table + condition
        return "select * from " + self.table

    def __sql_insert(self):
        return "insert into " + self.table + "(name,password) values(%s,%s)"


if __name__ == '__main__':
    from dict_server.dir_model.user_model import UserModel

    test = UserController('Account_test', 'account_local_test')
    print(test.register(UserModel("user03", "123456")))
    print(test.login("user03", "12345"))
