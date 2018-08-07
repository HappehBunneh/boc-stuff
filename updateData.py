import MySQLdb

class Database():
    def __init__(self):
        self.user = 'root'
        self.pwd = 'raspberry'
        self.database = 'data'
        self.table = 'data'
        self.db = MySQLdb.connect('localhost', self.user, self.pwd, self.database)
        self.curs = self.db.cursor()
        self.sql = 'drop table data;'
        self.curs.execute(self.sql)
        self.db.commit()
        self.sql = 'create table test (ID int NOT NULL AUTO_INCREMENT, current FLOAT, power FLOAT, temperature FLOAT, voltage FLOAT, PRIMARY KEY(ID));'
        self.curs.execute(self.sql)
        self.db.commit()

    def update(self, current, power, temperature, voltage):
        self.sql = 'insert into data (current, power, temperature, voltage) values (' + ','.join([str(i) for i in [current, power, temperature, voltage]]) + ')'
        self.curs.execute(self.sql)
        self.db.commit()