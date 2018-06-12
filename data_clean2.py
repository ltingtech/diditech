# _*_coding:utf-8_*_

import datetime
import db_connect as db
import os
import os.path


def data_clean():
    connection = db.db_connection()
    # 起始日期
    start_time = '2016-01-01 00:00:00'
    while start_time < '2016-01-31 00:30:00':
        print start_time
        day_order_table = start_time.split(' ')[0].replace('-', '_') + "_order_data_copy"      # 每天的记录表
        cursor = connection.cursor()
        f = open(start_time.split(' ')[0].replace('-', '_') + ".txt", 'w')
        day_start_time = start_time.split(' ')[0] + ' 00:00:00'
        day_end_time = start_time.split(' ')[0] + ' 0:59:59'
        day_deadline = start_time.split(' ')[0] + ' 23:59:59'
        while day_end_time <= day_deadline:
            sql = "SELECT  order_id,driver_id,passenger_id,dest_district_hash,time_slice FROM " + \
                  day_order_table + " WHERE TIME>'" +\
                  day_start_time + "' AND TIME<='" + day_end_time + "' ORDER BY passenger_id,TIME"
            # sql = "SELECT order_id,driver_id,passenger_id,dest_district_hash,time_slice " \
            #       "FROM 2016_01_01_order_data_copy WHERE passenger_id='00156d54838c42117ddc25cf5bf330bc' ORDER BY time"
            print sql
            try:
                cursor.execute(sql)
                order_results = cursor.fetchall()
                is_first_record = True
                for record in order_results:
                    if is_first_record:
                        is_first_record = False
                        last_order_id = record[0]
                        last_drive_id = record[1]
                        last_pass_id = record[2]
                        last_dest_hash = record[3]
                        last_time_slice = record[4]
                        continue
                    else:
                        next_order_id = record[0]
                        next_drive_id = record[1]
                        next_pass_id = record[2]
                        next_dest_hash = record[3]
                        next_time_slice = record[4]
                        if next_pass_id == last_pass_id and next_time_slice == last_time_slice:
                            # 应答情况都为空，目的地一样
                            if next_drive_id == 'NULL' and last_drive_id == 'NULL' and next_dest_hash == last_dest_hash:
                                delete_sql = "DELETE FROM " + day_order_table + \
                                             " WHERE order_id='" + last_order_id + "';\n"
                                f.write(delete_sql)
                            # 去的地方一样，且应答情况不一样
                            if next_drive_id != last_drive_id and next_dest_hash == last_dest_hash:
                                if next_drive_id == 'NULL':   # 哪种情况为空就删除哪条记录
                                    delete_sql = "DELETE FROM " + day_order_table + \
                                                 " WHERE order_id='" + next_order_id + "';\n"
                                    f.write(delete_sql)
                                if last_drive_id == 'NULL':
                                    delete_sql = "DELETE FROM " + day_order_table + \
                                                 " WHERE order_id='" + last_order_id + "';\n"
                                    f.write(delete_sql)
                            # 去的地方不一样，应答情况也不一样，
                            if next_drive_id != last_drive_id and next_dest_hash != last_dest_hash:
                                continue
                        last_order_id = next_order_id
                        last_drive_id = next_drive_id
                        last_pass_id = next_pass_id
                        last_dest_hash = next_dest_hash
                        last_time_slice = next_time_slice
                        # last_time = next_time
                        # last_time_second = next_time_second
            except Exception:
                print 'Wrong!!!'
            day_t1 = datetime.datetime.strptime(day_start_time, "%Y-%m-%d %H:%M:%S")
            day_t2 = datetime.datetime.strptime(day_end_time, "%Y-%m-%d %H:%M:%S")
            day_start_time = str(day_t1 + datetime.timedelta(hours=1))
            day_end_time = str(day_t2 + datetime.timedelta(hours=1))

        f.close()
        cursor.close()
        # 日期按天自增
        t1 = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        start_time = str(t1 + datetime.timedelta(days=1))
    connection.close()


def data_clean2():
    connection = db.db_connection()
    # 起始日期
    start_time = '2016-01-01 00:00:00'
    while start_time < '2016-01-31 00:30:00':
        print start_time
        day_order_table = start_time.split(' ')[0].replace('-', '_') + "_order_data"  # 每天的记录表
        cursor = connection.cursor()
        f = open(start_time.split(' ')[0].replace('-', '_') + ".txt", 'w')
        day_start_time = start_time.split(' ')[0] + ' 00:00:00'
        day_end_time = start_time.split(' ')[0] + ' 0:59:59'
        day_deadline = start_time.split(' ')[0] + ' 23:59:59'
        while day_end_time <= day_deadline:
            sql = "SELECT  order_id,driver_id,passenger_id,dest_district_hash,time_slice FROM " + \
                  day_order_table + " WHERE TIME>'" + \
                  day_start_time + "' AND TIME<='" + day_end_time + "' ORDER BY passenger_id,TIME"
            # sql = "SELECT order_id,driver_id,passenger_id,dest_district_hash,time_slice " \
            #       "FROM 2016_01_01_order_data WHERE passenger_id='00156d54838c42117ddc25cf5bf330bc' ORDER BY time"
            print sql
            try:
                cursor.execute(sql)
                order_results = cursor.fetchall()
                is_first_record = True
                null_order_id_list = []
                for record in order_results:
                    if is_first_record:
                        is_first_record = False
                        last_order_id = record[0]
                        last_drive_id = record[1]
                        last_pass_id = record[2]
                        last_dest_hash = record[3]
                        last_time_slice = record[4]
                        if last_drive_id == 'NULL':
                            null_order_id_list.append(last_drive_id)
                        continue
                    else:
                        next_order_id = record[0]
                        next_drive_id = record[1]
                        next_pass_id = record[2]
                        next_dest_hash = record[3]
                        next_time_slice = record[4]
                        if next_pass_id == last_pass_id and next_time_slice == last_time_slice:
                            if next_drive_id == 'NULL':
                                null_order_id_list.append(next_drive_id)
                            else:
                                continue
                        else:    # 如果用户跳变，或者是时间片跳变
                            if len(null_order_id_list) > 1:
                                for i in range(1, len(null_order_id_list)):
                                    delete_sql = "DELETE FROM " + day_order_table + \
                                                 " WHERE order_id='" + null_order_id_list[i] + "';\n"
                                    f.write(delete_sql)
                            null_order_id_list = []
                            if next_drive_id == 'NULL':
                                null_order_id_list.append(next_drive_id)
                            else:
                                continue
                        last_order_id = next_order_id
                        last_drive_id = next_drive_id
                        last_pass_id = next_pass_id
                        last_dest_hash = next_dest_hash
                        last_time_slice = next_time_slice
                        # last_time = next_time
                        # last_time_second = next_time_second
                if len(null_order_id_list) > 1:
                    for i in range(1, len(null_order_id_list)):
                        delete_sql = "DELETE FROM " + day_order_table + \
                                     " WHERE order_id='" + null_order_id_list[i] + "';\n"
                        f.write(delete_sql)
                    null_order_id_list = []
            except Exception:
                print 'Wrong!!!'
            day_t1 = datetime.datetime.strptime(day_start_time, "%Y-%m-%d %H:%M:%S")
            day_t2 = datetime.datetime.strptime(day_end_time, "%Y-%m-%d %H:%M:%S")
            day_start_time = str(day_t1 + datetime.timedelta(hours=1))
            day_end_time = str(day_t2 + datetime.timedelta(hours=1))

        f.close()
        cursor.close()
        # 日期按天自增
        t1 = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        start_time = str(t1 + datetime.timedelta(days=1))
    connection.close()


def execute_in_sql(file_name, save_file):
    print file_name
    connection = db.db_connection()
    cursor = connection.cursor()
    r_f = open(file_name, 'r')
    w_f = open(save_file, 'w')
    line = r_f.readline()
    delete_sql_head = "DELETE FROM " + file_name.split('E:\\data_clean\\')[1].split('.')[0] + \
                      "_order_data_copy WHERE order_id IN "
    

    print delete_sql_head
    order_id_list = []
    while line:
        if line != '':
            order_id_list.append(line.split('=')[1].split(';')[0])
        line = r_f.readline()
    delete_sql_condi = '(' + ','.join(order_id_list) + ');\n'
    sql = delete_sql_head + delete_sql_condi
    try:
        cursor.execute(sql)
        connection.commit()
    except Exception:
        print 'Wrong'
    print '*'*10
    w_f.write(sql)
    connection.close()
    r_f.close()
    w_f.close()


def execute_all_sql(file_dir):
    for parent, dirName, file_names in os.walk(file_dir):
        for sql_file in file_names:
            execute_in_sql(file_dir + sql_file, 'no_use.txt')

data_clean2()
# execute_all_sql("E:\\data_clean\\")
# execute_in_sql('2016_01_01.txt', 'kk.txt')
