import MySQLdb
import MySQLdb.cursors

# interact with a MySQL database
class CrawlerDB:  

    def __init__(self, host, username, password, databse): 
        """
        Connect to MySQL server
        :type host: str
        :type username: str
        :type password: str
        :type database: str
        :rtype: None
        """

        try:
            self.db = MySQLdb.connect(host = host, user = username, passwd = password, db = databse, use_unicode = True, charset = 'utf8', cursorclass = MySQLdb.cursors.DictCursor);
            self.cursor = self.db.cursor()
        except Exception as e:
            print('Cannot connect to MySQL server: ' + str(e))


    def checkExists(self, table):
        """
        Check if the table with the given name already exists in the database
        :type table: str
        :rtype: int
        """

        query = self.showQuery(table)
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if result:
                return 1
            else:
                return 0
        except Exception as e:
            print('Cannot show tables: ' + str(e))

    def showQuery(self, table):
        """
        Provide the query for SHOW operation
        :type table: str
        :rtype: str
        """

        query = """SHOW TABLES LIKE '{0}';"""
        return (query.format(table))

    def createQuery(self, mydict):
        """
        Provide the query for CREATE operation
        :type mydict: dict
        :rtype: str
        """

        query = """CREATE TABLE IF NOT EXISTS {0} ({1});"""

        d = dict(mydict) 
        table = d.pop('table')
        columns = []
        for key, value in  d.items():
            columns.append(key + ' ' + value)
        columns = ','.join(columns)

        return (query.format(table, columns))

    def insertQuery(self, mydict):
        """
        Provide the query for INSERT operation
        :type mydict: dict
        :rtype: str
        """

        query = """INSERT INTO {0} ({1}) VALUES ({2});"""

        d = dict(mydict)  
        table = d.pop('table')
        columns = ','.join(d.keys())
        placeholders = ','.join(['%s']* len(d)) 
        values = d.values()

        return (query.format(table, columns, placeholders), values)

    def selectQuery(self, mydict):
        """
        Provide the query for SELECT operation
        :type mydict: dict
        :rtype: str
        """

        querySimple = """SELECT {0} FROM {1};"""
        queryWhere = """SELECT {0} FROM {1} WHERE {2};"""

        d = dict(mydict)
        table = d.pop('table')
        if 'columns' in d.keys():
            columns = d.pop('columns')
        else:
            columns = '*'
        if 'op' in d.keys():
            operator = d.pop('op')
        else:
            operator = 'AND'
        whereClause = ('=%s ' + operator + ' ').join(d.keys())
        whereClause += '=%s'
        values = d.values()

        if len(d.keys()) > 0:
            return(queryWhere.format(columns, table, whereClause), values)
        else:
            return(querySimple.format(columns, table), values)

    def updateQuery(self, mydict):
        """
        Provide the query for UPDATE operation
        :type mydict: dict
        :rtype: str
        """

        querySimple = """UPDATE {0} SET {1};"""
        queryWhere = """UPDATE {0} SET {1} WHERE {2};"""

        d = dict(mydict)
        table = d.pop('table')
        setDict = d.pop('set')
        whereDict = d.pop('where')
        if 'op' in d.keys():
            operator = d.pop('op')
        else:
            operator = 'AND'
        setColumn = ('=%s, ').join(setDict.keys())
        setColumn += '=%s'
        setValue = setDict.values()
        whereColumn = ('=%s ' + operator + ' ').join(whereDict.keys())
        whereColumn += '=%s'
        whereValue = whereDict.values()
        params = list(setValue) + list(whereValue)

        if len(list(whereDict.keys())) > 0:
            return (queryWhere.format(table, setColumn, whereColumn), params)
        else:
            return (querySimple.format(table, setColumn), params)
            
    def create(self, createDictionary):
        """
        Create table
        :type createDictionary: dict
        :rtype: str
        """

        query = self.createQuery(createDictionary)
        try:
            self.cursor.execute(query)
        except Exception as e:
            print('Cannot create table: ' + str(e))

    def insert(self, insertDictionary):
        """
        Insert a record into the database
        :type insertDictionary: dict
        :rtype: str
        """

        if isinstance(insertDictionary, dict):
            query, params = self.insertQuery(insertDictionary)
            try:
                self.cursor.execute(query, params)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print('Cannot insert into table: ' + str(e))
        else:
            try:
                self.cursor.execute(insertDictionary)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print('Cannot insert into table: ' + str(e))

    def select(self, selectDictionary):
        """
        Read records from the database
        :type selectDictionary: dict
        :rtype: str
        """

        if isinstance(selectDictionary, dict):
            query, params = self.selectQuery(selectDictionary)
            try:
                if len(params) > 0:
                    self.cursor.execute(query, params)
                else:
                    self.cursor.execute(query)
            except Exception as e:
                print('Cannot select from table: ' + str(e))
        else:
            try:
                self.cursor.execute(selectDictionary)
            except Exception as e:
                print('Cannot select from table: ' + str(e))

    def selectAll(self):
        """
        Fetch all search results
        :rtype: List[dict]
        """

        try:
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            print('Cannot fetch from table: ' + str(e))
            return None

    def selectOne(self):
        """
        Fetch one search result
        :rtype: dict
        """

        try:
            rows = self.cursor.fetchone()
            return rows
        except Exception as e:
            print('Cannot fetch from table: ' + str(e))
            return None

    def selectMany(self, many):
        """
        Fetch 'many' search results
        :type many: int
        :rtype: List[dict]
        """

        try:
            rows = self.cursor.fetchmany(many)
            return rows
        except Exception as e:
            print('Cannot fetch from table: ' + str(e))
            return None
        
    def update(self, updateDictionary):
        """
        Update required records from the database
        :type updateDictionary: dict
        :rtype: str
        """

        if isinstance(updateDictionary, dict):
            query, params = self.updateQuery(updateDictionary)
            try:
                self.cursor.execute(query, params)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print('Cannot update table: ' + str(e))
        else:
            try:
                self.cursor.execute(updateDictionary)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print('Cannot update table: ' + str(e))

    def disconect(self):
        """
        Disconnect from MySQL server
        :rtype: None
        """

        try:
            self.db.close()
        except Exception as e:
            print('Cannot close connection: ' + str(e))

    def rowcount(self):
        """
        The number of results
        :rtype: int
        """

        return self.cursor.rowcount