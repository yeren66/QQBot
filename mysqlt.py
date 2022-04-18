import pymysql
import pandas as pd
import datetime

class SQL:
    def __init__(self):
        self.user = 'root'
        self.password = 'gcgl1431'
        self.database = 'QQBot'
        self.encode = 'encode'
        try:
            self.db = pymysql.connect(host='localhost', port=3306, user=self.user, passwd=self.password, db=self.database, autocommit=True)
            self.cursor = self.db.cursor()
            sql = f"CREATE TABLE IF NOT EXISTS { self.encode }(`qqaccount` INT(15) not null primary key, `qqname` VARCHAR(50) not null);"
            self.cursor.execute(sql)
            
            print("connect mysql succeed")
        except:
            try:
                self.db = pymysql.connect(host='localhost', port='3306', user=self.user, passwd=self.password)
                self.cursor = self.db.cursor()
                self.cursor.execute(f"CREATE DATABASE { self.database}")
                self.cursor.execute(f"USE { self.database}")
                print(f"connect mysql succeed, create database { self.database }")
            except:
                self.db = None
                self.cursor = None
                print("connect mysql failed")

    def check_connection(self):
        return self.cursor is not None

    def saveGroupMessage(self, QQgroup, groupname, QQ, nickname, content):
        # 用于t.py中的功能
        # 将群组中的消息存入表格，若为第一次存储则为其建立新表格
        # send_time_f = time.strftime("%Y%m%d%H%M%S", time.localtime(send_time))
        today = datetime.date.today()
        formatted_today=today.strftime('%y%m%d')
        table = str(groupname) + "_" +formatted_today
        sql = f"CREATE TABLE IF NOT EXISTS { table } (qq INT(15) not null, time DATETIME not null, content TEXT not null);"
        self.cursor.execute(sql) 
        sql = f"INSERT INTO { self.encode } (qqaccount, qqname) SELECT { QQgroup }, '{ groupname }' FROM DUAL WHERE NOT EXISTS (SELECT qqaccount FROM {self.encode} WHERE qqaccount={QQgroup}); "
        self.cursor.execute(sql) 
        sql = f"INSERT INTO { self.encode } (qqaccount, qqname) SELECT { QQ }, '{ nickname }' FROM DUAL WHERE NOT EXISTS (SELECT qqaccount FROM {self.encode} WHERE qqaccount={QQ}); "
        self.cursor.execute(sql) 
        if QQ != '' and nickname != '' and content != '':
            sql = f"INSERT INTO { table } VALUES ({ QQ }, now(), '{ content }')"
            try:
                self.cursor.execute(sql)
                self.db.commit()
                return {"status": 1}
            except Exception as e:
                return {"status": 0, "err": e}
        else:
            return {"status": 0, "err": "QQ or msg is empty!"}

    def saveFriendMessage(self, QQ, nickname, content):
        # 用于t.py中的功能
        # 将好友发送的信息存入表中，若是第一次发送则为期创建新表格
        table = str(nickname)
        sql = f"CREATE TABLE IF NOT EXISTS { table } (time DATETIME, content TEXT);"
        self.cursor.execute(sql)
        sql = f"INSERT INTO { self.encode } (qqaccount, qqname) SELECT { QQ }, '{ nickname }' FROM DUAL WHERE NOT EXISTS (SELECT qqaccount FROM {self.encode} WHERE qqaccount={QQ}); "
        self.cursor.execute(sql) 
        if QQ != '' and nickname != '' and content != '':
            sql = f"INSERT INTO { table } VALUES (now(), '{ content }')"
            try:
                self.cursor.execute(sql)    
                self.db.commit()
                return {"status": 1}
            except Exception as e:
                return {"status": 0, "err": e}
        else:
            return {"status": 0, "err": "QQ or msg is empty!"}

    def get_num(self):
        # 继承来的，获取self.table中的信息条数
        sql = f"SELECT COUNT(*) FROM { self.table };"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return str(result[0][0])
        except:
            return "查询出错！"

    def command(self, command):
        # 继承来的，用于执行mysql语句（command中的内容）
        try:
            self.cursor.execute(command)
            result = self.cursor.fetchall()
            return str(result)
        except:
            return "指令错误！"

    def process(self, table_name):
        # 初稿，没有进行进一步的封装
        # 作用是获取黑暗降临表中的全部信息，封装成一个DataFrame返回
        sql = f"SELECT content FROM { table_name };"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        content = pd.DataFrame(list(result),columns=['content'])
        # print(content.head())
        return content

    def rank_message(self, word, table_name):
        # 初稿，没有进行进一步的封装
        # 作用是建立words表格，并将参数中的word存入表格，若表格中有相同的word，则times + 1
        table_name_ = "words_" + str(table_name)
        try:
            # 为rank_message函数建立表格
            sql = f"CREATE TABLE IF NOT EXISTS {table_name_} ( times INT(10), word VARCHAR(10) );"
            self.cursor.execute(sql)
            sql = f"INSERT INTO {table_name_} (times, word) SELECT '0', '{ word }' FROM DUAL WHERE NOT EXISTS (SELECT times FROM {table_name_} WHERE word = '{word}'); "
            self.cursor.execute(sql)
            # print(sql)
            sql = f"UPDATE {table_name_} SET times=times+1 WHERE word = '{word}';"
            self.cursor.execute(sql)
            # print(sql)
            return True
        except:
            return False

    def adjust(self, table_name):
        sql = f"DELETE FROM {table_name} WHERE content LIKE '%[%]%';"
        self.cursor.execute(sql)
        return

    def adjust_punctuation(self, table_name):
        punctuation = [',','.','?','/','：','，','。','《','》','、','‘','’','“','”','；','（','）',' ']
        for p in punctuation:
            self.delete_content(table_name, p)
    
    def delete_content(self, table_name, text):
        sql = f"DELETE FROM {table_name} WHERE word LIKE '%{text}%';"
        # print(sql)
        self.cursor.execute(sql)



# sql = SQL()
# sql.adjust_punctuation('words_黑暗降临_220418')
# ret = sql.rank_message("一夫一妻")
# print(ret)
# sql.process()
# sql.saveGroupMessage(115414, 'test', 1919810, 'bot', "hhhhhhh23333")

