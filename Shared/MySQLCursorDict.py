__author__ = 'root'
import mysql.connector
import mysql.connector.cursor


class MySQLCursorDict(mysql.connector.cursor.MySQLCursor):

  def fetchone(self):
    row = self._fetch_row()
    if row:
      return dict(zip(self.column_names, self._row_to_python(row)))
    return None

  def fetchall(self):
    row = self._fetch_row()
    if row:
      return dict(zip(self.column_names, self._row_to_python(row)))
    return None