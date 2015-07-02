

__author__ = 'root'
import MySQLdb
class Database(object):
    _iInstance = None
    class Singleton:
        def __init__(self):
            # add singleton variables here
            self.connection = MySQLdb.connect("127.0.0.1", "switch", "Potatohair51!", "switch")
    def __init__( self):
        if Database._iInstance is None:
            Database._iInstance = Database.Singleton()
        self._EventHandler_instance = Database._iInstance

    def __getattr__(self, aAttr):
        return getattr(self._iInstance, aAttr)

    def __setattr__(self, aAttr, aValue):
        return setattr(self._iInstance, aAttr, aValue)

class SwitchDatabase():
    def __init__(self):
        pass

    @staticmethod
    def get_connection():
        pass
