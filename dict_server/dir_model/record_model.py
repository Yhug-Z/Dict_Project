"""
    记录 数据 模型
"""


class RecordModel:
    def __init__(self, name, word, time=None, id_=None):
        self.name = name
        self.word = word
        self.time = time
        self.id = id_
