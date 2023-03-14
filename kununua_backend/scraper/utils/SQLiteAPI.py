import sqlite3
from django.utils.translation import gettext as _

class SQLiteAPI(object):
    
    def __init__(self, db_name):
        if not isinstance(db_name, str):
            raise ValueError(_("Database name must be a string"))
        
        self.db_name = db_name
        self.conn = self._open_connection()
        self.cursor = self._get_cursor()
    
    def _open_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
        except sqlite3.DatabaseError as e:
            print(e)
        return conn
    
    def _get_cursor(self):
        cursor = None
        try:
            cursor = self.conn.cursor()
        except sqlite3.DatabaseError as e:
            print(e)
        return cursor
    
    def create_table(self, table_name, columns):
        if not isinstance(table_name, str):
            raise ValueError(_("Table name must be a string"))
        if not isinstance(columns, str):
            raise ValueError(_("Columns must be a string"))
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, columns))
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(e)
    
    def insert_data(self, table_name, data):
        if not isinstance(table_name, str):
            raise ValueError(_("Table name must be a string"))
        if not isinstance(data, str):
            raise ValueError(_("Data must be a string"))
        try:
            self.cursor.execute("INSERT INTO {} VALUES ({})".format(table_name, data))
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(e)
    
    def update_data(self, table_name, data, condition):
        if not isinstance(table_name, str):
            raise ValueError(_("Table name must be a string"))
        if not isinstance(data, str):
            raise ValueError(_("Data must be a string"))
        if not isinstance(condition, str):
            raise ValueError(_("Condition must be a string"))
        try:
            self.cursor.execute("UPDATE {} SET {} WHERE {}".format(table_name, data, condition))
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(e)
    
    def delete_data(self, table_name, condition):
        if not isinstance(table_name, str):
            raise ValueError(_("Table name must be a string"))
        if not isinstance(condition, str):
            raise ValueError(_("Condition must be a string"))
        try:
            self.cursor.execute("DELETE FROM {} WHERE {}".format(table_name, condition))
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(e)
