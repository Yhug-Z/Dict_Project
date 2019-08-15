"""
    用户账号，密码数据模型
"""


class UserModer:
    """
    用户账号，密码数据模型
    """
    def __init__(self, name, password, id_=None):
        self.id = id_
        self.user_name = name
        self.password = password
