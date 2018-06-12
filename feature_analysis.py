# _*_coding:utf-8_*_
import matplotlib.pylab as pl
import db_connect as db


def feature_analysis(feature, district, days, save_dir):
    connection = db.db_connection()
    cursor = connection.cursor()
    sql_base = "SELECT %s FROM gap_table WHERE day='%s' AND district_id='%s' ORDER BY time_slice "
    colors = ['b', 'g', 'r', 'y', 'k', 'w', 'm']
    count = 0
    is_first = True
    for day in days:
        sql = sql_base % (feature, day, district)
        print sql
        result = []
        try:
            cursor.execute(sql)
            records = cursor.fetchall()
            for record in records:
                if record[0] is not None:
                    result.append(float(record[0]))
                else:
                    result.append(-1)
        except Exception:
            print 'wrong'
        result = data_supplement(result)
        # if is_first:
        #     pl.plot(result, color=colors[count % len(colors)], label=feature)
        #     is_first = False
        # else:
        #     pl.plot(result, color=colors[count % len(colors)])
        pl.plot(result, color=colors[count % len(colors)], label=day)
        count += 1
    pl.legend()
    pl.title(feature)
    fig_name = district + "_" + feature + ".png"
    pl.savefig(save_dir + fig_name)
    pl.close()

# 缺失数据补全
def data_supplement(result):
    for i, ele in enumerate(result):
        index = i
        if result[i] == -1:
            if index == 0:
                while index <= len(result)-1:
                    if result[index] != -1:
                        result[i] = result[index]
                        break
                    else:
                        index += 1
            else:
                if index == len(result)-1:
                    while index >=0:
                        if result[index] != -1:
                            result[i] = result[index]
                            break
                        else:
                            index -= 1
                else:
                    up_index = index + 1
                    down_index = index - 1
                    up_ele = -1
                    down_ele = -1
                    while up_index <= len(result) -1:
                        if result[up_index] != -1:
                            up_ele = result[up_index]
                            break
                        else:
                            up_index += 1
                    while down_index >= 0:
                        if result[down_index] != -1:
                            down_ele = result[down_index]
                            break
                        else:
                            down_index -= 1
                    if down_ele != -1 and up_ele != -1:
                        result[i] = (down_ele + up_ele) / 2
                    if down_ele != -1 and up_ele == -1:
                        result[i] = down_ele
                    if down_ele == -1 and up_ele != -1:
                        result[i] = up_ele
                    if down_ele == -1 and up_ele == -1:
                        print "wrongwrong"
        else:
            continue
    return result


# 衍生特征值入库
def feature_judge(sql_file):
    w_f = open(sql_file, 'w')
    w_f.write("DROP TABLE IF EXISTS `feature_judge`;\n")
    w_f.write("CREATE TABLE `feature_judge` (\n" +
              "`district_id` varchar(10) DEFAULT NULL,\n" +
              "`time_slice` varchar(20) DEFAULT NULL,\n " +
              "`district_code` varchar(10) DEFAULT NULL,\n" +
              "`time_slice_code` varchar(10)\n " +
              ");\n")
    code_1000 = ['1', '12', '16', '19', '20', '24', '25', '28', '29', '38', '42', '46', '53']
    code_1100 = ['4', '6',  '37']
    code_0100 = ['41']
    code_1010 = ['26']
    code_1110 = ['14', '23']
    code_1111 = ['7', '8', '48', '51']
    connection = db.db_connection()
    sql = "SELECT district_id,time_slice FROM gap_table ORDER BY district_id,time_slice"
    print sql
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        records = cursor.fetchall()
        insert_base = "insert  into `feature_judge`(`district_id`,`time_slice`,`district_code`,`time_slice_code`)"
        for record in records:
            district_id = record[0]
            time_slice = record[1]
            district_code = '0000'
            if district_id in code_0100:
                district_code = '0100'
            if district_id in code_1000:
                district_code = '1000'
            if district_id in code_1010:
                district_code = '1010'
            if district_id in code_1100:
                district_code = '1100'
            if district_id in code_1110:
                district_code = '1110'
            if district_id in code_1111:
                district_code = '1111'
            segment = time_slice.split('-')[3]
            time_slice_code = '0'  # 默认为0
            if segment >= '100':
                if segment <= '110':
                    time_slice_code = '4'
                else:
                    if '125' <= segment <= '135':
                        time_slice_code = '5'
            else:
                if '000' <= segment <= '030':
                    time_slice_code = '1'
                if '040' <= segment <= '060':
                    time_slice_code = '2'
                if '075' <= segment <= '095':
                    time_slice_code = '3'
            inser_value = "values ('" + district_id + "','" + time_slice + "','" +\
                          district_code + "','" + time_slice_code + "');\n"
            w_f.write(insert_base + inser_value)


    except Exception:
        print 'wrong!'
    w_f.write('commit;')
    cursor.close()
    connection.close()




def main():
    feature_judge('feature_judge.sql')
    # attribute = 'gap'
    # district = '51'
    # days = [str(i) for i in range(4, 9)]
    # feature_analysis(attribute, district, days)
    # save_dir = u"E:\\算法大赛\\分析结果图\\高峰图\\"
    # # district = ['24', '28', '46', '42', '27']
    # # district = ['0' + str(i) for i in range(1, 10)]
    # district = [str(i) for i in range(10, 67)]
    # # attributes = ['gap', 'temperature', 'weather', 'pm25', 'traffic3', 'traffic4']
    # attributes = ['gap']
    # days = [str(i) for i in range(4, 9)]
    # days += [str(i) for i in range(11, 16)]
    # for district_id in district:
    #     for attribute in attributes:
    #         feature_analysis(attribute, district_id, days, save_dir)

main()
