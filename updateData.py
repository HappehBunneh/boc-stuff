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
        self.sql = 'insert into data values(%d, %d, %d, %d)' % (current, power, temperature, voltage) 
        self.curs.execute(self.sql)
        self.db.commit()