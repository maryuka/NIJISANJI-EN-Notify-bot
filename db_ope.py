import mysql.connector 
import json
import logging
import os

class MySQLConnect:
    def __init__(self):
        '''
        DBの接続情報を保持する
        '''
        self.host       = os.environ['DB_HOST']
        self.port       = os.environ['DB_PORT']
        self.db         = os.environ['DB']
        self.user       = os.environ['DB_USER']
        self.password   = os.environ['DB_PASS']
        self.charset    = 'utf8'

    def _connect(self):
        conn = mysql.connector.connect(
            host        = self.host,
            port        = self.port,
            user        = self.user,
            password    = self.password,
            database    = self.db,
            charset     = self.charset,
            autocommit  = True
        )
        conn.ping(reconnect=True)
        return conn
    
    def execute(self, sql):
        '''
        execute SQL

        Parameters
        ----------
        sql : str
        '''
        try:
            conn = self._connect()
            cur = conn.cursor()
            cur.execute(sql)
            cur.close()
            conn.close()
        except mysql.connector.Error as e:
            logging.exception(f'database error: {e}')

    def execute_fetch(self, sql):
        '''
        execute SQL, and return the result

        Parameters
        ----------
        sql : str

        Returns
        ----------
        result : list
        '''
        try:
            conn = self._connect()
            cur = conn.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            cur.close()
            conn.close()
            return res
        except mysql.connector.Error as e:
            logging.exception(f'database error: {e}')

    def db_create(self):
        sql = 'CREATE TABLE IF NOT EXISTS daily_logs (id MEDIUMINT NOT NULL Auto_Increment PRIMARY KEY, date varchar(128), log text);'
        self.execute(sql)

    def db_insert(self,day_num_log, today):
        sql = f'INSERT INTO daily_logs (date, log) VALUES (\'{today}\', \'{json.dumps(day_num_log)}\');'
        self.execute(sql)

    def db_delete_table(self):
        sql = 'DROP TABLE IF EXISTS daily_logs;'
        self.execute(sql)

    def db_delete_exc_latest(self):
        sql = 'SET @mid = (SELECT max(id) from daily_logs)'
        self.execute(sql)
        sql = 'DELETE FROM daily_logs WHERE id != @mid;'
        self.execute(sql)

    def db_get_log(self,yesterday):
        '''
        get the yesterday' subscriber count data from the database

        Parameters
        ----------
        yesterday : str
            example: 2022-09-09
        
        Returns
        ----------
        result : dict
            yesterday's subscriber count data
            {name:subscriber count(int), ...}
            if there is no matching data , return None object
        '''
        result = self.execute_fetch(f'SELECT log FROM daily_logs WHERE date = \'{yesterday:s}\';')
        if result!=None:
            result = json.loads(result[0][0])
        return result