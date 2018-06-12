# _*_coding:utf-8_*_
import db_connect as db
import csv


def create_gap_table(sql_file):
    w_f = open(sql_file, 'w')
    create_table_sql = "create table `gap_table` (\n" + "`restrict_id` varchar(10),\n" + \
                       "`time_slice` varchar(10),\n" + \
                       "`gap` varchar(10)" + "\n);\n"
    print create_table_sql
    w_f.write(create_table_sql)
    select_sql = "SELECT start_district_id,time_slice FROM order_data WHERE driver_id='null'"
    connection = db.db_connection()
    cursor = connection.cursor()
    result_dic = {}
    try:
        cursor.execute(select_sql)
        record_results = cursor.fetchall()
        count = 0
        num = 0
        for record in record_results:
            if count > 10000:
                num += 1
                print '*'*10 + str(num)
                count = 0
            else:
                count += 1
            dic_key = record[0] + "#" + record[1]
            if dic_key in result_dic.keys():
                result_dic[dic_key] += 1
            else:
                result_dic[dic_key] = 1
    except Exception:
        print 'Wrong'
    if len(result_dic) > 0:
        count = 0
        num = 0
        for record in result_dic.iteritems():
            if count > 10000:
                num += 1
                print '-'*10 + str(num)
                count = 0
            else:
                count += 1
            dic_key = record[0]
            district_id = dic_key.split('#')[0]
            time_slice = dic_key.split('#')[1]
            dic_value = record[1]
            insert_sql = "insert into `gap_table` (`restrict_id`,`time_slice`,`gap`) values (" + \
                         "'" + district_id + "','" + time_slice + "','" + str(dic_value) + "');\n"
            w_f.write(insert_sql)
        w_f.write('commit;')
    cursor.close()
    connection.close()
    w_f.close()


def model_evaluate(csv_file):
    csv_file = file(csv_file, 'rb')
    reader = csv.reader(csv_file)
    connection = db.db_connection()
    cursor = connection.cursor()
    gap_dic = {}
    select_all_gap = 'SELECT * FROM gap_table'
    try:
        cursor.execute(select_all_gap)
        record_results = cursor.fetchall()
        for record in record_results:
            dic_key = record[0] + '#' + record[1]
            dic_value = int(record[2])
            gap_dic[dic_key] = dic_value
    except Exception:
        print 'Wrong'
    cursor.close()
    connection.close()
    test_record_dic = {}
    for line in reader:
        district_id = line[0]
        if district_id in test_record_dic.keys():
            test_record_dic[district_id].append(line[1] + '#' + line[2])
        else:
            test_record_dic[district_id] = [line[1] + '#' + line[2]]
    test_keys = test_record_dic.keys()
    evaluation_score = 0
    evaluation_score_district = 0
    for district in test_keys:
        district_gap_list = test_record_dic[district]
        for ele in district_gap_list:
            gap_key = district + '#' + ele.split('#')[0]
            evaluate_gap = float(ele.split('#')[1])
            if gap_key in gap_dic.keys():
                real_gap = gap_dic[gap_key]
            else:
                real_gap = 0
            if real_gap != 0:
                evaluation_score_district += abs((real_gap - evaluate_gap) / real_gap)
            else:
                continue
        evaluation_score_district /= len(district_gap_list)  # q的选择把所有的（包括为0的都考虑在内）
        evaluation_score += evaluation_score_district
    evaluation_score /= len(test_record_dic)
    return evaluation_score






# create_gap_table('gap_table.txt')
model_evaluate("C:\Users\\Administrator\\Desktop\\01_gdbt_gap.csv")

