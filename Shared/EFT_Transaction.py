from datetime import datetime
import sys

import MySQLdb


class Transaction():
    tran_gid = ""
    con = None
    d_req_timestamp = ""
    d_req = ""
    d_req_type = ""
    b_terminal_id = ""
    local_tran_date = ""
    local_tran_time = ""
    o_auth_no = ""
    d_res = None

    def __init__(self, tran_gid, con):
        self.con = con
        self.tran_gid = tran_gid
        self.d_req_timestamp = datetime.today()

        cur = self.con.cursor(MySQLdb.cursors.DictCursor)
        try:
            sql = """
                INSERT INTO terminals_eftpos
                    (tran_gid, d_req_timestamp, d_req)
                VALUES
                    ('%s', '%s', '%s')
                """ % (self.tran_gid, self.d_req_timestamp, self.d_req)
            # print sql
            cur.execute(sql)
            con.commit()

        except Exception:
            print "Initial Transaction Failed ", sys.exc_info()[0]
        finally:
            cur.close()

    def __repr__(self):
        return "<Transaction('%s')>" % self.tran_gid
