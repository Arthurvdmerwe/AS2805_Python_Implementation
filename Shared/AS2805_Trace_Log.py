__author__ = 'root'
from datetime import datetime
import string

import MySQLdb

import Tran_Type
import ASResponseCodes


def LogTrace(iso, host, mti, result):

    d = datetime.now()
    hex_dump = dumphex(iso.getNetworkISO())
    iso_dump = iso.dumpFields()

    if result != '':
        trasaction_result = ASResponseCodes.GetISOResponseText(result)
    else:
        trasaction_result = ''

    transaction_type = Tran_Type.GetMessagesescription(mti)

    sql = """ INSERT INTO switch_office.host_trace_log(
                        created,
                        host_data,
                        iso,
                        binary_data,
                        trasaction_result,
                        transaction_type
                        )

            VALUES ("%s", "%s", "%s", "%s", "%s", "%s")
          """ % (d, host, MySQLdb.escape_string(iso_dump), MySQLdb.escape_string(hex_dump), trasaction_result, transaction_type)
    return sql



def dumphex(s):
  global i
  hex_str = 'Binary Data: \n'

  str = ""
  for i in range(0,len(s)):
    if s[i] in string.whitespace:
      str += '.'
      continue
    if s[i] in string.printable:
      str = str + s[i]
      continue
    str += '.'
  bytes = map(lambda x: '%.2x' % x, map(ord, s))
  print
  for i in xrange(0,len(bytes)/16):
    hex_str +=  '    %s' % string.join(bytes[i * 16:(i + 1) * 16])
    hex_str +=  '    %s\n' % str[i*16:(i+1)*16]
  hex_str += '    %-51s' % string.join(bytes[(i + 1) * 16:])
  hex_str += '%s\n' % str[(i+1)*16:]

  return hex_str