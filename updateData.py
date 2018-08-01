import MySQLdb

class Database():
    def __init__(self):
        self.user = 'root'
        self.pwd = 'raspberry'
        self.database = 'data'
        self.table = 'data'
        self.db = MySQLdb.connect('localhost', self.user, self.pwd, self.database)
        self.curs = self.db.cursor()

    def update(self, current, power, temperature, voltage):
        self.sql = 'insert into data values(' + ','.join([str(i) for i in [current, power, temperature, voltage]]) + ')'
        print self.sql
        self.curs.execute(self.sql)
        self.db.commit()