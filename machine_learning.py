from sklearn.ensemble import GradientBoostingRegressor
import numpy as np
from sklearn.cross_validation import train_test_split


def feature2matraix(filename):
    fr = open(filename)
    array_lines = fr.readlines()
    line_length = len(array_lines)
    return_matrix = np.zeros((line_length, 26))   # 初始化为0矩阵，26列
    class_label_vector = []
    index = 0
    for line in array_lines:
        line = line.strip()
        list_form_line = line.split(',')
        try:

            return_matrix[index, :] = list_form_line[0:26]         # 特征存储
            class_label_vector.append(int(list_form_line[-1]))   # 分类结果存储
            index += 1
        except Exception :
            print 'ERROR'
            print index

    return return_matrix, class_label_vector


def main():
    mat, label = feature2matraix("data_file/poi.csv")   # 获取特征，及结果
    label = np.asarray(label)
    feature_train, feature_test, target_train, target_test = train_test_split(mat, label, test_size=0.3, random_state=0)
    clf = GradientBoostingRegressor(n_estimators=40, max_features=3)  # 构造函数
    print clf
    clf.fit(mat, label)
    score = clf.score(feature_test, target_test)
    print score

    print 10*clf.feature_importances_
    feature_important = 10*clf.feature_importances_

    result = []
    for i, ele in enumerate(feature_important):
        result.append((i+1, ele))
    result.sort(key=lambda x: x[1], reverse=True)
    print result

# important_idx=np.where(feature_important>0)
# sorted_index=np.argsort(feature_important[important_idx][::-1])
# feature_important.sort()
# print feature_important
# print sorted_index