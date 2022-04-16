import pymysql

class SQL:
    def __init__(self):
        self.user = 'root'
        self.password = 'gcgl1431'
        self.database = 'QQBot'
        self.encode = 'encode'
        try:
            self.db = pymysql.connect(host='localhost', port=3306, user=self.user, passwd=self.password, db=self.database)
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
        # send_time_f = time.strftime("%Y%m%d%H%M%S", time.localtime(send_time))
        table = str(groupname)
        sql = f"CREATE TABLE IF NOT EXISTS { table } (qq INT(15) not null, time DATETIME not null, content TEXT not null);"
        self.cursor.execute(sql) 
        sql = f"INSERT INTO { self.encode } (qqaccount, qqname) SELECT '{ QQgroup }', '{ groupname }' FROM DUAL WHERE NOT EXISTS (SELECT qqaccount FROM {self.encode} WHERE qqaccount={QQgroup}); "
        self.cursor.execute(sql) 
        sql = f"INSERT INTO { self.encode } (qqaccount, qqname) SELECT '{ QQ }', '{ nickname }' FROM DUAL WHERE NOT EXISTS (SELECT qqaccount FROM {self.encode} WHERE qqaccount={QQ}); "
        self.cursor.execute(sql) 
        if QQ != '' and nickname != '' and content != '':
            sql = f"INSERT INTO { table } VALUES ('{ QQ }', now(), '{ content }')"
            try:
                self.cursor.execute(sql)
                self.db.commit()
                return {"status": 1}
            except Exception as e:
                return {"status": 0, "err": e}
        else:
            return {"status": 0, "err": "QQ or msg is empty!"}

    def saveFriendMessage(self, QQ, nickname, content):
        table = str(nickname)
        sql = f"CREATE TABLE IF NOT EXISTS { table } (time DATETIME, content TEXT);"
        self.cursor.execute(sql)
        sql = f"INSERT INTO { self.encode } (qqaccount, qqname) SELECT '{ QQ }', '{ nickname }' FROM DUAL WHERE NOT EXISTS (SELECT qqaccount FROM {self.encode} WHERE qqaccount={QQ}); "
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
        sql = f"SELECT COUNT(*) FROM { self.table }"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return str(result[0][0])
        except:
            return "查询出错！"

    def command(self, command):
        try:
            self.cursor.execute(command)
            result = self.cursor.fetchall()
            return str(result)
        except:
            return "指令错误！"

# sql = SQL()
# sql.saveGroupMessage(115414, 'test', 1919810, 'bot', "hhhhhhh23333")
