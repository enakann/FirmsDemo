import sqlite3
import os
import logging


# from utils import export


class NoDataAvailableException (Exception):
    pass


class DBDoesntExistException (Exception):
    pass


logger = logging.getLogger ("aggregator")


def logger_with_exception_handling(msg, *exp):
    def decorator(f):
        def inner(*args, **kwargs):
            ret = None
            try:
                logger.info (msg)
                ret = f (*args, **kwargs)
            except exp as e:
                print (e)
                logger.exception (e)
            return ret
        
        return inner
    
    return decorator


# @export
class DataStore:
    """
    Generic Datastore Class for Firms2
    """
    
    def __init__(self, db):
        self.db = db
        self.cur = None
        self.conn = None
    
    def __enter__(self):
        self.connect ()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close ()
    
    @logger_with_exception_handling ("Connecting to db", Exception)
    def connect(self):
        """ connect to db"""
        if not self.db:
            raise DBDoesntExistException (self.db)
        self.conn = sqlite3.connect (self.db)
        self.cur = self.conn.cursor ()
    
    def insert(self, query, data):
        """ insert data into table"""
        
        logger.info ("Insert called :{} with {}".format (query, data))
        try:
            self.cur.execute (query, data)
            self.conn.commit ()
        except Exception as e:
            logger.exception ("Insert of {} failed due to {}".format (data, e))
            return False
        return True
    
    def insert_rows(self, query, data):
        """ inserting multiple rows """
        
        logger.info ("Insert called :{} with {}".format (query, data))
        try:
            self.cur.executemany (query, data)
            self.conn.commit ()
        except Exception as e:
            logger.exception ("Insert of {} failed due to {}".format (data, e))
            return False
        return True
    
    def select_data(self, query, bind):
        """ select query  """
        data = list ()
        try:
            self.cur.execute (query, bind)
            data = self.cur.fetchall ()
            logger.info ("following items retrieved {}".format (data))
            if not data:
                raise NoDataAvailableException (query, bind, data)
        except Exception as e:
            logger.exception ("Select failed :{}-{} due to {}".format (query, bind, e))
        return data
    
    def delete(self, query, bind):
        logger.info ("delete called :{} with {}".format (query, bind))
        try:
            self.cur.execute (query, bind)
            self.conn.commit ()
        except Exception as e:
            logger.exception ("delete : {}  of {} failed due to {}".format (query, bind, e))
            return False
        return True
    
    @logger_with_exception_handling ("Closing connection", Exception)
    def close(self):
        self.conn.close ()
    
    @logger_with_exception_handling ("creating table", Exception)
    def create_table(self):
        self.cur.execute (
            "CREATE TABLE IF NOT EXISTS contacts (id integer primary key autoincrement,first_name varchar(10),last_name varchar(10),email varchar(10),mobile varchar(10))")


if __name__ == '__main__':
    with DataStore (r"C:\Users\navkanna\PycharmProjects\FirmsDemo\Aggregator\Aggregator\test.db") as dbobj:
        ret = dbobj.select_data ("select * from contacts where first_name=:1", ("navi",))
        print (ret)
        # dbobj.create_table()
    
    # d = DataStore("test.db")
    # d.create_table()
    # d.insert("insert into contacts values(?,?,?,?,?)", [3, "navi", "kannan", "nav@gmail.com", 1111])
    # ret = d.select_data("select * from contacts where first_name=:1", ("navi",))
    # print(ret)

    # with DataStore("test.db") as dbobj:
    # ret=dbobj.insert("insert into contacts values(?,?,?,?,?)", [3, "navi", "kannan", "nav@gmail.com", 1111])
    # print(ret)
    #  dbobj.insert ("insert into contacts values(?,?,?,?,?)", [3, "divi", "kannan", "nav@gmail.com", 1111])
    #   print(dbobj.select_data ("select * from contacts where first_name=:1", ("divi",)))
    # ret = dbobj.select_data ("select * from contacts where first_name=:1", ("navi",))
    # dbobj.delete("delete from contacts where first_name=:1",("divi",))
    # ret = dbobj.select_data ("select * from contacts where first_name=:1", ("divi",))
    # print(ret)
    # if ret:
    #    print("data is there")
    # else:
    #    print("data is not there")
        
        
    
