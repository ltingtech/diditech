# _*_coding:utf-8

import os
import os.path
import csv


def calculate_predict_gap(demand_dir, supply_dir, gap_save_file):
    g_f = open(gap_save_file, 'w')
    demand_predict_files = []
    supply_predict_files = []
    for parent, dirName, file_names in os.walk(demand_dir):
        demand_predict_files = file_names
    for parent, dirName, file_names in os.walk(supply_dir):
        supply_predict_files = file_names
    if len(demand_predict_files) == len(supply_predict_files):
        gap = []
        for i in range((len(demand_predict_files))):
            demand_file = demand_dir + "/" + demand_predict_files[i]
            supply_file = supply_dir + "/" + supply_predict_files[i]
            d_f = open(demand_file)
            s_f = open(supply_file)
            demand = []
            supply = []
            demand_contents = d_f.readlines()
            for ele in demand_contents:
                demand.append(float(ele))
            supply_contents = s_f.readlines()
            for ele in supply_contents:
                supply.append(float(ele))
            gap_file = []
            if len(demand) == len(supply):
                for j in range(len(demand)):
                    if demand[j] - supply[j] < 0:
                        gap.append(0)
                    else:
                        gap.append(demand[j] - supply[j])
                    if demand[j] - supply[j] > 820:
                        print u'文件名%s %s, line %d' % (demand_file, supply_file, j)
                    gap_file.append(str(demand[j] - supply[j]) + ' ')
            gap_content = ','.join(gap_file)
            g_f.write(gap_content + '\n')
        g_f.close()
        csv_file1 = file('data_file/11.csv', 'rb')
        csv_file2 = file('data_file/22.csv', 'wb')
        reader = csv.reader(csv_file1)
        writer = csv.writer(csv_file2)
        index = 0
        print 'max gap'
        print max(gap)
        for line in reader:
            line[len(line)-1] = gap[index]
            writer.writerow(line)
            index += 1
        csv_file1.close()
        csv_file2.close()
    else:
        print u'文件个数不一样'


calculate_predict_gap("demand", "supply", 'gap.txt')