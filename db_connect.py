# _*_coding:utf-8_*_

import MySQLdb


def db_connection():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='root', db='diditech', charset='utf8')
    return conn


def select_sql(sql):
    db = db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        # result = cursor.fetchall()
        # for row in result:
        #     print row[1]
    except Exception:
        print 'error'
    db.close()


# select_sql("DELETE FROM 2016_01_01_order_data_copy WHERE order_id='0262fdae65c4b8c46876ad553683d940'")
