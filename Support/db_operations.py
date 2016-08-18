__author__ = 'sf'

import sys
import MySQLdb

sys.path.append('../')
import config

class DBOperations:
    def __init__(self):
        self.db_address = config.DB_ADDRESS
        self.db_user = config.DB_USER
        self.db_pass = config.DB_PASS
        pass

    def execute_sql(self, dbname, sql, sql_type="select"):
        """
        execute sql and return result
        :param dbname: dbname to execute sql
        :param sql: Mysql string
        :param sql_type: sql type is select or update, default is select
        :return: return "fail" if execute sql failed,
                 return select result when select sql, otherwise return "success"
        """
        try:
            db = MySQLdb.connect(self.db_address, self.db_user, self.db_pass, dbname)
            db.set_character_set('utf8')
            cursor = db.cursor()

            cursor.execute(sql)

            if sql_type == "select":
                result = cursor.fetchall()
            else:
                result = 'success'
            db.close()
            return result
        except Exception, e:
            print e, "sql==", sql
            return "fail"

if __name__ == "__main__":
    db_operation = DBOperations()
    sql = "select count(*) from com_db_sf_task where 1"
    print db_operation.execute_sql("db_sf", sql, "select")
