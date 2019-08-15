"""
    查找单词
"""
import pymysql


class WordsController:
    def __init__(self, database, table, host='localhost', port=3306, user='root', password='123456',
                 charset='utf8'):
        self.db = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                                  charset=charset)
        self.cur = self.db.cursor()
        self.table = table

    def find(self,word):
        self.cur.execute(self.__select_by_word(),word)
        meat=self.cur.fetchone()
        if meat:
            return meat[0]
        return None

    def __select_by_word(self):
        return "select mean from "+self.table+" where word=%s "
