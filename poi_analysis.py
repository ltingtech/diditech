# _*_coding:utf-8_*_

import db_connect as db
import matplotlib.pylab as pl


def get_poi_map():
    connection = db.db_connection()
    sql = 'SELECT * FROM cluster_map'
    cursor = connection.cursor()
    dic = {}
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            key = row[1]
            value = row[0]
            dic[key] = value
    except Exception:
        print 'error'
    connection.close()
    return dic


def statics_by_poi(output_file):
    poi_map = get_poi_map()
    connection = db.db_connection()
    cursor = connection.cursor()
    f = open(output_file, 'w')
    for poi_id in poi_map.keys():
        poi_hash = poi_map[poi_id]
        select_sql = "SELECT poi_class FROM poi_data where district_hash='%s'" % poi_hash
        cursor.execute(select_sql)
        result = cursor.fetchone()[0]
        detail_eles = result.split(' ')
        region_count_map = {}
        for ele in detail_eles:
            index = ele.find('#')
            if index == -1:        # if doesn't exits symbol #, then split by :
                key = int(ele.split(':')[0])
                value = int(ele.split(':')[1])
                region_count_map[key] = value
            else:
                key = int(ele.split('#')[0])
                leng = len(ele.split('#'))
                value = int(ele.split('#')[leng-1].split(':')[1])  # if exits #, take the last element as the number
                if key in region_count_map.keys():
                    region_count_map[key] += value
                else:
                    region_count_map[key] = value
        max_region_index = max(region_count_map.items(), key=lambda x:x[0])[0]
        content1 = str(poi_id) + '#' + str(max_region_index) + '#'
        content2 = ''
        for key in region_count_map.keys():
            content2 += str(key) + ':' + str(region_count_map[key]) + ' '
        content = content1 + content2
        f.write(content)
        f.write('\n')
    connection.close()
    f.close()


# 对每个区域内每种类型的区域内poi的数量建表
def convert_to_sql(file_name, output_file):
    f_read = open(file_name, 'r')
    f_write = open(output_file, 'w')
    create_table_sql = "DROP TABLE IF EXISTS `poi_region`;\ncreate table `poi_region` (\n" + "`poi_id` varchar(10),\n"
    var = []
    for i in range(1, 26):
        var.append("`" + str(i) + "` " + "varchar (10)")
    var.append("`" + 'total_num' + "` " + "int")
    create_table_sql_var = ",\n".join(var)
    create_table_sql += create_table_sql_var + "\n);\n"
    f_write.write(create_table_sql)
    line = f_read.readline()
    sql_base = "insert into `poi_region` "
    while line:
        poi_id = line.split('#')[0]
        item_list = ["`poi_id`"]
        value_list = ["'" + poi_id + "'"]
        total_num = 0
        for ele in line.split('#')[2].split(' '):
            if ele == '\n':
                break
            item_list.append("`" + ele.split(':')[0] + "`")
            total_num += int(ele.split(':')[1])
            value_list.append("'" + ele.split(':')[1] + "'")
        item_list.append("`total_num`")
        value_list.append("'" + str(total_num) + "'")
        sql_item_list = '(' + ','.join(item_list) + ')'
        sql_value_list = '(' + ','.join(value_list) + ')'
        sql = sql_base + sql_item_list + ' values' + sql_value_list + ';\n'
        f_write.write(sql)
        line = f_read.readline()
    f_write.write('commit;')
    f_write.close()


def calculate_poi_feature(feature_file):
    connection = db.db_connection()
    cursor = connection.cursor()
    f = open(feature_file, 'w')
    # poi_sql = 'select * from poi_region_order'
    poi_sql = 'select * from poi_region'
    cursor.execute(poi_sql)
    region_num_list = []
    records = cursor.fetchall()
    for record in records:
        # num = 0
        # for i in range(1, len(record)-1):
        #     num += int(record[i])
        num = int(record[len(record) - 1])
        region_num_list.append(num)
    max_region_num = max(region_num_list)
    print max_region_num
    for i, record in enumerate(records):
        line = [record[0]]
        region_num = int(region_num_list[i])
        for j in range(1, len(record)-1):
            if record[j] is not None:
                line.append(str(float(record[j])/region_num))  # the ratio in district_id
            else:
                line.append('0')
        line.append(str(region_num/float(max_region_num)))  # the ratio of district_id in all
        line.append(str(region_num))
        line_content = ','.join(line)
        f.write(line_content + '\n')
    f.close()
    connection.close()


def convert_feature_sql(feature_file, output_file):
    f_read = open(feature_file, 'r')
    f_write = open(output_file, 'w')
    create_table_sql = "DROP TABLE IF EXISTS `poi_feature`;\ncreate table `poi_feature` (\n" + "`poi_id` varchar(10),\n"
    var = []
    for i in range(1, 26):
        # if i < 10:
        #     var.append("`0" + str(i) + "` " + "varchar (20)")
        # else:
        #     var.append("`" + str(i) + "` " + "varchar (20)")
        var.append("`" + str(i) + "` " + "varchar (20)")
    var.append("`" + "total_num_ratio" + "` " + "varchar(20)")
    var.append("`" + "total_num" + "` " + "varchar(20)")
    create_table_sql_var = ",\n".join(var)
    create_table_sql += create_table_sql_var + "\n);\n"
    f_write.write(create_table_sql)
    line = f_read.readline()
    sql_base = "insert into `poi_feature` "
    item_list = ['`poi_id`']
    for i in range(1, 26):
        # if i < 10:
        #     item_list.append("`0" + str(i) + "` ")
        # else:
        #     item_list.append('`' + str(i) + '`')
        item_list.append('`' + str(i) + '`')
    item_list.append('`total_num_ratio`')
    item_list.append('`total_num`')
    sql_item_list = '(' + ','.join(item_list) + ')'
    while line:
        value_list = line.split(',')
        value_list[len(value_list)-1] = value_list[len(value_list)-1].split('\n')[0]
        sql_value_list = "('" + "','".join(value_list) + "')"
        sql = sql_base + sql_item_list + ' values' + sql_value_list + ';\n'
        f_write.write(sql)
        line = f_read.readline()
    f_write.close()


def show_region_ratio():   # 显示不同类型的场所在不同poi区域中的比值规律
    connection = db.db_connection()
    sql = "SELECT * FROM poi_feature ORDER BY poi_id"
    cursor = connection.cursor()
    result = {}
    try:
        cursor.execute(sql)
        records = cursor.fetchall()
        for record in records:
            for j in range(1, 26):
                if j in result.keys():
                    result[j].append(float(record[j]))
                else:
                    result[j] = [float(record[j])]
    except Exception:
        print 'wrong'
    for key in result.keys():
        value = result[key]
        pl.plot(value, 'g', label='region ' + str(key),)
        pl.legend()
        pl.savefig('data_file\\' + str(key) + '.png')
        pl.close()









# statics_by_poi('poi.txt')
# convert_to_sql('data_file\poi.txt', 'data_file\sql.sql')
# calculate_poi_feature('data_file\poi_feature.txt')
# convert_feature_sql("data_file\poi_feature.txt", 'data_file\\featur_sql.sql')
# show_region_ratio()
show_district_gap(district_id='01')




