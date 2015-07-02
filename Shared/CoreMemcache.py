__author__ = 'root'
import sys

import MySQLdb
import memcache


memc = memcache.Client(['127.0.0.1:11212'], debug=1)
try:
    conn = MySQLdb.connect (host = "localhost",
                            user = "switch",
                            passwd = "Potatohair51!",
                            db = "switch")
except MySQLdb.Error, e:
     print "Error %d: %s" % (e.args[0], e.args[1])
     sys.exit (1)







def GetRecord(tran_gid):
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    try:
        record = memc.get(tran_gid)
        if not record:
            sql = 'select * from core_node WHERE tran_gid = "%s"  limit 1' % tran_gid
            count = cur.execute(sql)
            if count == 1:
                row = cur.fetchone()
                memc.set(row['tran_gid'], row, 30)
                print "Got From Database"
                return row

        else:
            print "Got From Memcached"
            return record

    finally:
        cur.close()





def UpdateRecord(data):
    pass

def InsertRecord(query, tran_gid):
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    try:
            sql = 'select * from core_node WHERE tran_gid = "%s"  limit 1' % tran_gid
            count = cur.execute(sql)
            if count == 1:
                row = cur.fetchone()
                memc.set(row['tran_gid'], row, 30)
                return row

    finally:
        cur.close()



core_transaction = GetRecord('123123123213')
print core_transaction