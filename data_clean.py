# _*_coding:utf-8_*_
import time
import datetime
import db_connect as db


def data_clean():
    connection = db.db_connection()
    # 起始日期
    start_time = '2016-01-01 00:00:00'
    # 结束时间
    end_time = '2016-01-01 23:59:59'
    while start_time < '2016-01-31 00:00:00':
        print start_time
        pass_ordernum_table = start_time.split(' ')[0].replace('-', '_') + "_pass_orderNum"       # 用户记录数表
        day_order_table = start_time.split(' ')[0].replace('-', '_') + "_order_data"      # 每天的记录表
        pass_id_list = []
        select_pass_id_sql = "SELECT passenger_id FROM " + pass_ordernum_table + " WHERE orderNum>1"
        cursor = connection.cursor()
        try:
            cursor.execute(select_pass_id_sql)
            results = cursor.fetchall()
            for pass_id in results:
                pass_id_list.append(pass_id[0])
        except Exception:
            print 'Error!'
        if len(pass_id_list) > 0:
            f = open("start_time.split(' ')[0].replace('-', '_')" + ".txt", 'w')
            for id_ele in pass_id_list:         # 对每个用户进行处理
                select_pass_order_sql = "SELECT order_id,TIME FROM " + day_order_table + \
                                        " WHERE passenger_id='" + id_ele + "' ORDER BY TIME "
                order_id_time_dic = {}
                try:
                    cursor.execute(select_pass_order_sql)
                    order_id_time_results = cursor.fetchall()
                    for ele in order_id_time_results:
                        order_id_time_dic[ele[0]] = ele[1]         #订单号和时间组成字典
                except Exception:
                    print 'WrongWrong!!'
                if len(order_id_time_dic) > 0:
                    sorted_dic = sorted(order_id_time_dic.iteritems(), key=lambda x: x[1])
                    time_list = []
                    order_id_list = []
                    for i in range(len(sorted_dic)):
                        time_list.append(sorted_dic[i][1])
                        order_id_list.append(sorted_dic[i][0])
                    # last_time = time.strptime(time_list[0], "%Y-%m-%d %H:%M:%S")
                    last_time = time_list[0]

                    last_time_second = int(time.mktime(last_time.timetuple()))
                    for i in range(1, len(time_list)):
                        # next_time = time.strptime(time_list[i], "%Y-%m-%d %H:%M:%S")
                        next_time = time_list[i]
                        next_time_second = int(time.mktime(next_time.timetuple()))
                        time_gap = next_time_second - last_time_second
                        last_time_second = next_time_second
                        if time_gap < 10*60:
                            order_id = order_id_list[i]
                            delete_sql = "DELETE FROM " + day_order_table + " WHERE order_id='" + order_id + "';\n"
                            f.write(delete_sql)
        f.close()
        cursor.close()
        # 日期按天自增
        t1 = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        t2 = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        start_time = str(t1 + datetime.timedelta(days=1))
        end_time = str(t2 + datetime.timedelta(days=1))
    connection.close()

data_clean()

