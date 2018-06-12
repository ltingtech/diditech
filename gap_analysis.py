# _*_coding:utf-8_*_

import db_connect as db
import matplotlib.pylab as pl
import datetime

# 画出每个区域的所有gap走势图
def show_district_gap(district_id):
    connection = db.db_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM gap_table WHERE district_id='" + district_id + \
          "' AND time_slice> '2016-01-15-001' AND time_slice<'2016-01-21-144'ORDER BY time_slice"
    print sql
    gap_list = []
    try:
        cursor.execute(sql)
        records = cursor.fetchall()
        for record in records:
            if float(record[2]) > 40:
                gap_list.append(40)
            else:
                gap_list.append(float(record[2]))
    except Exception:
        print 'wrong'
    cursor.close()
    connection.close()
    if len(gap_list) > 0:
        pl.plot(gap_list, 'g', label='gap')
        pl.legend()
        pl.show()


# 计算每个时间片gap的整体平均值
def show_mean_gap():
    start_time = '2016-01-02 00:00:00'
    end_time = '2016-01-20 00:00:00'
    date_list = []
    while start_time <= end_time:
        date_list.append(start_time.split(' ')[0])
        t1 = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        start_time = str(t1 + datetime.timedelta(days=1))
    connection = db.db_connection()
    cursor = connection.cursor();
    sql = "SELECT * FROM gap_table WHERE district_id='01' ORDER BY time_slice"
    gap_dic = {}
    try:
        cursor.execute(sql)
        records = cursor.fetchall()
        for record in records:
            key = record[1]
            value = record[2]
            if key not in gap_dic.keys():
                gap_dic[key] = value
    except Exception:
        print 'wrong'
    result = []
    for i in range(1, 145):
        total = 0
        for ele in date_list:
            if i < 10:
                key = ele + '-00' + str(i)
            else:
                if i < 100:
                    key = ele + '-0' + str(i)
                else:
                    key = ele + '-' + str(i)
            if key in gap_dic.keys():
                total += float(gap_dic[key])
        result.append(total/float(len(date_list)))
    index = range(1, 145)
    pl.plot(index, result, 'g', label='mean_gap')
    pl.legend()
    pl.show()


show_mean_gap()