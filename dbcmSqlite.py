import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        return self.cur   # return cursor for convenience

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()   # commit if no exception
        else:
            self.conn.rollback() # rollback on error
        self.conn.close()
