import sqlite3
import os


class DataStore:
    """
    high level support for doing this and that.
    """
    
    def __init__(self, db):
        self.db = db
        self.cur = None
        self.conn = None
    
    def __enter__(self):
        print("enter context manager")
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def connect(self):
        """ connect to db"""
        print("connection called")
        try:
            self.conn = sqlite3.connect(self.db)
            self.cur = self.conn.cursor()
        except Exception as e:
            raise e
    
    def insert(self, query, data):
        print ("insert called")
        try:
            self.cur.execute(query, data)
            self.conn.commit()
        except Exception as e:
            print(e)
            raise e
            return False
        return True
    
    def insert_rows(self, query, data):
        """
        high level support for doing this and that.
        """
        self.cur.executemany(query, data)
        self.conn.commit()
    
    def select_data(self, query, bind):
        """
        high level support for doing this and that.
        """
        self.cur.execute(query, bind)
        data = self.cur.fetchall()
        return data
    
    def delete(self,query,bind):
        try:
            self.cur.execute(query,bind)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True
        
        
    
    def create_table(self):
        self.connect()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS validator (id integer primary key autoincrement,first_name varchar(10),last_name varchar(10),email varchar(10),mobile varchar(10))")
    
    def close(self):
        print("connection is close")
        self.conn.close()


if __name__ == '__main__':
    #d = DataStore("test.db")
    #d.create_table()
    #d.insert("insert into contacts values(?,?,?,?,?)", [3, "navi", "kannan", "nav@gmail.com", 1111])
    #ret = d.select_data("select * from contacts where first_name=:1", ("navi",))
    #print(ret)
    
    with DataStore("test.db") as dbobj:
        #ret=dbobj.insert("insert into contacts values(?,?,?,?,?)", [3, "navi", "kannan", "nav@gmail.com", 1111])
        #print(ret)
        dbobj.insert ("insert into contacts values(?,?,?,?,?)", [3, "divi", "kannan", "nav@gmail.com", 1111])
        print(dbobj.select_data ("select * from contacts where first_name=:1", ("divi",)))
        #ret = dbobj.select_data ("select * from contacts where first_name=:1", ("navi",))
        dbobj.delete("delete from contacts where first_name=:1",("divi",))
        ret = dbobj.select_data ("select * from contacts where first_name=:1", ("divi",))
        print(ret)
        #if ret:
        #    print("data is there")
        #else:
        #    print("data is not there")
        
        
    
