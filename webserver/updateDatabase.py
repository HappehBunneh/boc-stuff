import MySQLdb
from random import randint
import time

db = MySQLdb.connect('localhost', 'root', 'raspberry', 'data')
curs=db.cursor()

while True:
    current, voltage, temp, power = randint(0,100), randint(0, 100), randint(0, 100), randint(0, 100)
    sql = 'insert into data values(%d, %d, %d, %d)' % (current, voltage, temp, power) 
    curs.execute(sql)
    db.commit()
    time.sleep(1)
