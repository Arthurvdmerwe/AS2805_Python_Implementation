from datetime import datetime

import MySQLdb


class Transaction():

    tran_gid = ""
    con = None
    d_req_timestamp = ""
    Handled_Request = ""
    Request = None
    Response = None


    def __init__(self, tran_gid, con):
        self.con = con
        self.tran_gid = tran_gid
        self.d_req_timestamp = datetime.today()

        cur = self.con.cursor()
        try:
            sql = """
                INSERT INTO core_node
                    (tran_gid, d_req_timestamp)
                VALUES
                    ('%s', '%s')
                """ % (self.tran_gid, self.d_req_timestamp)
            # print sql
            cur.execute(sql)


        except:
            print "Initial Transaction Failed"
        finally:
            cur.close()

    def __repr__(self):
        return "<Transaction('%s')>" % self.tran_gid
