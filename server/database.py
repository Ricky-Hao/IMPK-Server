import sqlite3
import os
from hashlib import md5
from .logger import logging

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Database:
    def __init__(self):
        self.db_name = 'server.db'
        self.db_path = os.path.join(path, self.db_name)
        self.log = logging.getLogger('Database')
        self.databaseInitial()

    def databaseInitial(self):
        if not os.path.exists(self.db_path):
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute('''CREATE TABLE user 
                          (ID INTEGER PRIMARY KEY autoincrement ,
                          USERNAME TEXT NOT NULL ,
                          PASSWORD TEXT NOT NULL ,
                          TIMESTAMP TimeStamp NOT NULL DEFAULT (datetime('now','localtime')))''')

            cur.execute('''
                      CREATE TABLE friends
                      (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                      USERNAME TEXT NOT NULL ,
                      FRIEND TEXT NOT NULL)''')

            cur.execute('''
                      CREATE TABLE cert
                      (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
                      USERNAME TEXT NOT NULL ,
                      CERT TEXT NOT NULL)''')

            conn.commit()
            conn.close()

    def quote(self, data_list):
        for i in range(len(data_list)):
            data_list[i] = "'{0}'".format(data_list[i])
        return ", ".join(data_list)

    def and_where(self, data_dict):
        temp_list = []
        for key in data_dict.keys():
            temp_list.append("{0}='{1}'".format(key, data_dict[key]))

        if len(temp_list) == 1:
            return temp_list[0]
        else:
            return ' and '.join(temp_list)

    def deleteOne(self, table, where='1=1'):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        result = cur.execute('delete from {0} where {1}'.format(table, where))
        cur.close()
        conn.commit()
        conn.close()
        return result

    def fetchOne(self, column, table, where='1=1'):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        result = cur.execute("select {0} from {1} where {2}".format(column, table, where)).fetchone()
        cur.close()
        conn.close()
        return result

    def fetchAll(self, column, table, where='1=1'):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        result = cur.execute("select {0} from {1} where {2}".format(column, table, where)).fetchall()
        cur.close()
        conn.close()
        return result

    def insertOne(self, table, field_list, value_list):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        result = cur.execute("insert into {0}({1}) values({2})".format(table, field_list, self.quote(value_list)))
        cur.close()
        conn.commit()
        conn.close()
        return result

    def addUser(self, username, password):
        password = md5(password.encode()).hexdigest()
        if self.fetchOne('*', 'user', self.and_where({'username':username})) is None:
            self.insertOne('user', 'USERNAME, PASSWORD', [username, password])
            return True
        return False

    def addCert(self, username, cert_data):
        if self.fetchOne('*', 'cert', self.and_where({'username':username})) is None:
            self.insertOne('cert', 'USERNAME, CERT', [username, cert_data])
            return True
        return False

    def fetchCert(self, username):
        return self.fetchOne('cert', 'cert', self.and_where({'username':username}))

    def checkUser(self, username, password):
        result = self.fetchOne('*', 'user', self.and_where({'username':username}))
        self.log.debug(result)
        if result is not None:
            if password == result[2]:
                return True
        return False

    def addFriend(self, username, friend):
        self.log.debug('Add friend {0}:{1}.'.format(username, friend))
        if self.fetchOne('*', 'friends', self.and_where({'username':username, 'friend':friend})) is None:
            self.insertOne('friends', 'USERNAME, FRIEND', [username, friend])
            return True
        return False

    def fetchFriend(self, username):
        return self.fetchAll('friend', 'friends', self.and_where({'username':username}))

    def delFriend(self, username, friend):
        return self.deleteOne('friends', self.and_where({'username':username, 'friend':friend}))


db = Database()