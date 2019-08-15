"""
创建一个数据库 dict
create database dict charset=utf8;
创建一个表 words
将单词本中的单词插入表中
 id     word     mean
 create table words (id smallint primary key auto_increment,word varchar(28) not null,mean text);
"""

import pymysql
import re

f = open('dict.txt') # 打开文件

# 连接数据库
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     password = '123456',
                     database = 'dict',
                     charset='utf8')

# 创建游标 (操作数据库语句,获取查询结果)
cur = db.cursor()

# 数据库操作
sql = "insert into words (word,mean) values (%s,%s)"
for line in f:
    tup = re.findall(r'(\S+)\s+(.*)',line)[0]
    try:
        cur.execute(sql,tup)
        db.commit()
    except:
        db.rollback()

f.close()
# 关闭游标和数据库
cur.close()
db.close()