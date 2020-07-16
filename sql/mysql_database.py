import mysql.connector as ms
from mysql.connector import errorcode

class mysql_db():
    def __init__(self,host='localhost',user='root',passwd='19900925',db='yoloV4'):
        self.host=host
        self.user=user
        self.passwd=passwd
        self.db=db
        self.connected=False

    def connect(self):
        try:
            self.mydb=ms.connect(host=self.host,user=self.user,passwd=self.passwd,database=self.db)
        except ms.Error as err:
            if err.errno==errorcode.ER_ACCESS_DENIED_ERROR:
                return 'Something is wrong with your mysql user name or password'
            elif err.errno==errorcode.ER_BAD_DB_ERROR:
                self.mydb=ms.connect(host=self.host,user=self.user,passwd=self.passwd)
                self.mycursor=self.mydb.cursor()
                self.mycursor.execute('CREATE DATABASE '+self.db)
                return self.connect()
            else:
                return 'connect mysql error'
        else:
            self.mycursor=self.mydb.cursor()
            self.connected=True
            return 'connect mysql ok'

    def discocnnect(self):
        if self.connected:
            self.mydb.close()

    def create_table(self,name):
        if self.connected and self.mydb.is_connected():
            try:
                self.mycursor.execute('CREATE TABLE `'+name+'` (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, message VARCHAR(255))')
            except ms.Error as err:
                if err.errno==errorcode.ER_TABLE_EXISTS_ERROR:
                    print('table already exists')
                else:
                    print(err.msg)
                return False
            else:
                return True

    def insert_data(self,table,data):
        if self.connected and self.mydb.is_connected():
            sql=('INSERT INTO `'+table+'` (`message`) VALUES (%s)')
            val=(data,)
            try:
                self.mycursor.execute(sql,val)
                self.mydb.commit()
            except ms.Error as err:
                print(err.msg)
                return False
            else:
                return True

        
if __name__=='__main__':
    test=mysql_db()
    print(test.connect())
    import time
    tablename=time.strftime('%Y-%m-%d/%H:%M:%S')
    print(test.create_table(tablename))
    print(test.insert_data(tablename,"b'hairpin 0.82'"))

