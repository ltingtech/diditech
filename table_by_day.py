# _*_coding:utf-8_*_

import datetime
import db_connect as db


def extract_data_by_day():
    connection = db.db_connection()
    # 起始日期
    start_time = '2016-01-01 00:00:00'
    # 结束时间
    end_time = '2016-01-01 23:59:59'
    while start_time < '2016-01-31 00:00:00':
        sql_head = "CREATE TABLE "+start_time.split(' ')[0].replace('-', '_') + "_order_data" + \
                   " AS SELECT * FROM order_data "
        # sql_head = "CREATE TABLE " + start_time.split(' ')[0].replace('-', '_') + \
        #            "_pass_orderNum AS SELECT COUNT(*) orderNum,passenger_id FROM " + \
        #            start_time.split(' ')[0].replace('-', '_') + "_order_data GROUP BY passenger_id"
        sql_condition = "where  time<'"
        sql_condition += end_time
        sql_condition += "' and time>'"
        sql_condition += start_time + "'"
        sql = sql_head + sql_condition
        print sql
        print sql_head
        try:
            cursor = connection.cursor()
            cursor.execute(sql)
            # cursor.execute(sql_head)
            cursor.close()
        except Exception:
            print 'Wrong!'
        # 日期按天自增
        t1 = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        t2 = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        start_time = str(t1 + datetime.timedelta(days=1))
        end_time = str(t2 + datetime.timedelta(days=1))
    connection.close()

extract_data_by_day()

