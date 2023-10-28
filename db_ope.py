# https://resanaplaza.com/2021/09/15/%E3%80%90-%E3%82%B3%E3%83%94%E3%83%9A%E3%81%A7ok%E3%80%91%EF%BC%99%E5%89%B2%E3%81%AE%E6%A9%9F%E8%83%BD%E3%82%92%E7%B6%B2%E7%BE%85%EF%BC%81pyton%E3%81%8B%E3%82%89postgresql%E3%82%92%E6%89%B1%E3%81%86/
import psycopg2
 
class PostgreConnect:
    '''
    ostgreSQのヘルパークラス
    Parameters
    '''
    GET_TABLE_LIST_QUERY = "SELECT t.* FROM (SELECT TABLENAME,SCHEMANAME,'table' as TYPE from PG_TABLES UNION SELECT VIEWNAME,SCHEMANAME,'view' as TYPE from PG_VIEWS) t WHERE TABLENAME LIKE LOWER('{0}') and SCHEMANAME like LOWER('{1}') and TYPE like LOWER('{2}');"
    GET_COLUMN_LIST_QUERY = "SELECT TABLE_NAME,COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME like LOWER('{0}') and TABLE_SCHEMA like LOWER('{1}') ORDER BY ORDINAL_POSITION;"
    GET_ALTER_TABLE_QUERY = "ALTER TABLE {0} ADD {1};"
    GET_RENAME_TABLE_QUERY = "alter table {0} rename to {1};"
    
    def __init__(self,host,dbname,user,password,port=5432):
        '''
        DBの接続情報を保持する
        Parameters
        ----------
        host : str
        　  ホスト名
        dbname : str
            DB名
        user : str
            ユーザー名
        password : str
            パスワード
        port : integer
            ポート
        '''
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
    
    def __connect(self):
        return psycopg2.connect("postgresql://{user}:{password}@{host}:{port}/{dbname}".format(user=self.user, password=self.password, host=self.host, port=self.port, dbname=self.dbname))
    
    def execute(self,sql):
        '''
        SQLを実行し、結果を取得する
        Parameters
        ----------
        columns : str
            実行したいSQL
        '''
        try:
            print(sql)
            conn = self.__connect()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
        except(Exception, psycopg2.Error) as e:
            print('database error', e)

    def execute_all(self,sqls):
        '''
        複数のSQLをトランザクション配下で実行する
        Parameters
        ----------
        columns : strs
            実行したいSQLのリスト
        '''
        conn = self.__connect()
        cur = conn.cursor()
        try:
            for sql in sqls:
                cur.execute(sql)
            conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
        cur.close()
        conn.close()
    
    def execute_query(self,sql):
        '''
        select 系のSQLを実行し、結果を全て取得する
        Parameters
        ----------
        columns : str
            実行したいSQL
        Returns
        ----------
        data: list
            １行分をタプルとし、複数行をリストとして返す
            <例> [('RX100','Sony',35000),('RX200','Sony',42000)]
        '''
        try:
            conn = self.__connect()
            cur = conn.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            cur.close()
            conn.close()
            return res
        except(Exception, psycopg2.Error) as e:
            print('エラーが発生', e)
    
    def execute_scalor(self,sql):
        '''
        結果の値が１つしかないSQLを実行し、結果を取得する
        Parameters
        ----------
        columns : str
            実行したいSQL
        Returns
        ----------
        res:
            実行結果により返された値
        '''
        try:
            conn = self.__connect()
            cur = conn.cursor()
            cur.execute(sql)
            res = cur.fetchone()
            cur.close()
            conn.close()
            return res if res != None else None
        except(Exception, psycopg2.Error) as e:
            print('エラーが発生', e)
    
    def create(self,tablename,columns,primarykey = '',isdrop=False):
        '''
        テーブルを作成する
        Parameters
        ----------
        columns : str
            「列名」又は「列名＋型」をカンマ区切りで指定
            <例> 'product text,price int,maker,year'
        primarykey: str
            プライマリーキーをカンマ区切りで指定
            <例> 'product,year'
        '''
        if isdrop :
            self.drop(tablename)
        pkey = ',PRIMARY KEY({0})'.format(primarykey) if primarykey != '' else ''
        sql = 'CREATE TABLE {0}({1} {2});'.format(tablename,columns,pkey)
        self.execute(sql)
    
    def exists(self,tablename):
        '''
        指定したテーブル、又はビューの有無を判定する
        Parameters
        ----------
        columns : str
            実行したいSQL
        Returns
        ----------
            テーブル又はビューが存在すればTrue 存在しなければ False
        '''
        res = self.execute_scalor('SELECT relname FROM pg_class WHERE relkind = \'r\' AND relname = \'{}\';'.format(tablename))
        return False if res == None else True
    
    def drop(self,tablename):
        '''
        指定されたテーブルが存在すれば削除、無ければ何もしない
        Parameters
        ----------
        tablename : str
            削除したいテーブル名
        '''
        if self.exists(tablename):
            self.execute("DROP TABLE {};".format(tablename))

    def rename(self,old_tablename,new_tablename):
        '''
        テーブル名を変更する
        Parameters
        ----------
        old_tablename : str
            変更前のテーブル名
        new_tablename : str
            変更後のテーブル名
        '''
        self.execute(self.GET_RENAME_TABLE_QUERY.format(old_tablename,new_tablename))
    
    def add_column(self,tablename,columns):
        '''
        テーブル名を変更する
        Parameters
        ----------
        tablename : str
            テーブル名
        columns : str
            「列名」又は「列名＋型」をリスト形式で指定
            <例> ['product varchar','price numeric(5,2)','maker integer']
        '''
        for column in columns:
            self.execute(self.GET_ALTER_TABLE_QUERY.format(tablename,column))
    
    def get_table_list(self,table_type=""):
        '''
        登録されているテーブルの一覧を取得する
        Parameters
        ----------
        table_type : str
            'table' => テーブルのみ、'view' => ビューのみ、'' => テーブルとビューの両方
        Returns
        ----------
        res:str
            リスト形式のテーブル名一覧
            <例>  ['talbe1','table2','table3']
        '''
        res = self.execute_query(self.GET_TABLE_LIST_QUERY.format('%%',self.scheme,'%' + table_type + '%'))
        return [name[0] for name in res]
    
    def get_column_type(self,tablename):
        '''
        指定したテーブルのカラムと型を一覧で取得する
        Parameters
        ----------
        tablename : str
            テーブル名
        Returns
        ----------
        res:str
            リスト形式でカラム名と型のタプルを返す
            <例>  [('column1','int'),('column2','text'),('column3',real)]
        '''
        res = self.execute_query(self.GET_COLUMN_LIST_QUERY.format(tablename,self.scheme))
        return [(name[1],name[2]) for name in res]
    
    def get_column_list(self,tablename):
        '''
        指定したテーブルのカラム名を一覧で取得する
        Parameters
        ----------
        tablename : str
            テーブル名
        Returns
        ----------
        res:str
            リスト形式のカラム名一覧
            <例>  ['column1','column2','column3']
        '''
        res = self.execute_query(self.GET_COLUMN_LIST_QUERY.format(tablename,self.scheme))
        return [name[1] for name in res]