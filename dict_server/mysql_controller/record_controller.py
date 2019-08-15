"""
    记录 控制器
"""
import pymysql


class RecordController:
    def __init__(self, database, table, host='localhost', port=3306, user='root', password='123456',
                 charset='utf8'):
        self.db = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                                  charset=charset)
        self.cur = self.db.cursor()
        self.table = table

    def add_record(self, target):
        try:
            self.cur.execute(self.__insert_sql(), [target.name, target.word])
            self.db.commit()
        except Exception as e:
            print("inster failure..", target.name)
            print(e)
            self.db.rollback()
            return

    def __insert_sql(self):
        return "insert into " + self.table + " (name,word) " + " values (%s,%s)"

    def find_record_by_user(self, name):
        self.cur.execute(self.__select_sql(), name)
        return self.cur.fetchmany(10)

    def __select_sql(self):
        return "select name,word from " + self.table + " where name=%s order by time desc"
