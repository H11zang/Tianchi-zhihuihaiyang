import csv
import pandas as pd
import os
import numpy as np

#输出csv文件
def write_csv(csv_name,list,csv_N):
    test = pd.DataFrame(columns=csv_name, data=list)
    test.to_csv(csv_N, encoding='gbk', index=None)

def sum_list(list):
    sum = 0
    for i in range(len(list)):
        sum += float(list[i])
    return sum

def feature_hour(state):
    if state == "train":
        csv_N = 'dataset_train/hour_2nd.csv'
        path = 'dataset_train/hour_ratio.csv'
    if state == "test":
        csv_N = 'dataset_test/hour_2nd.csv'
        path = 'dataset_test/hour_ratio.csv'
    with open(path) as f:
        reader = csv.reader(f)
        reader_list = list(reader)
        out_list = []
        csv_name = ['0T5_vs_8T12', '8T12_vs_13T18', '0T5_vs_13T18','0T5_vs_19t23', '8T12_vs_19t23', '13T18_vs_19t23', 'ratio_9t22']
        for i in range(1,len(reader_list)):
            ratio_0t5 = sum_list(reader_list[i][0:6])
            ratio_8t12 = sum_list(reader_list[i][6:13])
            ratio_13t18 = sum_list(reader_list[i][13:19])
            ratio_19t23 = sum_list(reader_list[i][19:])
            ratio_9t22 = sum_list(reader_list[i][9:23])
            h_0T5_vs_8T12 = 0
            h_8T12_vs_13T18 = 0
            h_0T5_vs_13T18 = 0
            h_0T5_vs_19t23 = 0
            h_8T12_vs_19t23 = 0
            h_13T18_vs_19t23 = 0
            if ratio_8t12 != 0:
                h_0T5_vs_8T12 = ratio_0t5/ratio_8t12
            if ratio_13t18 != 0:
                h_8T12_vs_13T18 = ratio_8t12/ratio_13t18
                h_0T5_vs_13T18 = ratio_0t5/ratio_13t18
            if ratio_19t23 != 0:
                h_0T5_vs_19t23 = ratio_0t5/ratio_19t23
                h_8T12_vs_19t23 = ratio_8t12/ratio_19t23
                h_13T18_vs_19t23 = ratio_13t18/ratio_19t23
            use_list = [h_0T5_vs_8T12,h_8T12_vs_13T18,h_0T5_vs_13T18,h_0T5_vs_19t23,h_8T12_vs_19t23,h_13T18_vs_19t23]
            out_list += [use_list+[ratio_9t22]]
    write_csv(csv_name, out_list, csv_N)


def feature_direction(state):
    if state == "train":
        csv_N = 'dataset_train/direction_2nd.csv'
        path = 'dataset_train/direction_ratio.csv'
    if state == "test":
        csv_N = 'dataset_test/direction_2nd.csv'
        path = 'dataset_test/direction_ratio.csv'
    with open(path) as f:
        reader = csv.reader(f)
        reader_list = list(reader)
        out_list = []
        for i in range(1,len(reader_list)):
            ratio_6 = []
            for j in range(12):
                ratio_6 += [sum_list(reader_list[i][j*3:j*3+3])]
            direction_6 = 12 - ratio_6.count(0)
            max_index = reader_list[i].index(max(reader_list[i]))
            direction_max_ratio = 0
            if max_index >=9 and max_index <= 27 and sum_list(reader_list[i][max_index-9:max_index+8]) != 0:
                direction_max_ratio = sum_list(reader_list[i][max_index-4:max_index+4])/sum_list(reader_list[i][max_index-9:max_index+8])
            if max_index >=4 and max_index <9 and sum_list(reader_list[i][:18]) != 0:
                direction_max_ratio = sum_list(reader_list[i][max_index-4:max_index+4])/sum_list(reader_list[i][:18])
            if max_index <4 and sum_list(reader_list[i][:18]) != 0:
                direction_max_ratio = sum_list(reader_list[i][:9])/sum_list(reader_list[i][:18])
            if max_index >27 and max_index <32 and sum_list(reader_list[i][18:36]) != 0:
                direction_max_ratio = sum_list(reader_list[i][max_index-4:max_index+4])/sum_list(reader_list[i][18:36])
            if max_index >=32 and sum_list(reader_list[i][18:36]) != 0:
                direction_max_ratio = sum_list(reader_list[i][27:36])/sum_list(reader_list[i][18:36])

            direction_list = []
            for j in range(len(reader_list[i])):
                direction_list += [float(reader_list[i][j])]
            direction_df = pd.DataFrame(direction_list)
            direction_dict = {'max': 0, 'min': 100000, 'arg': 0, 'median': 0, 'more': 0, 'std': 0, 'sum': 0, 'mad': 0}
            if len(reader_list[i]) != 0:
                direction_dict['max'] = direction_df.max().values[0]
                direction_dict['min'] = direction_df.min().values[0]
                direction_dict['arg'] = direction_df.mean().values[0]
                direction_dict['median'] = direction_df.median().values[0]
                direction_dict['std'] = direction_df.std().values[0]
                direction_dict['more'] = direction_df.mode().values[0]
                direction_dict['sum'] = direction_df.sum().values[0]
                direction_dict['mad'] = direction_df.mad().values[0]
            if direction_dict['min'] == 100000:
                direction_dict['min'] = 0
            direction_var = 0
            if direction_dict['arg'] != 0:
                direction_var = direction_dict['std'] / direction_dict['arg']

            add = [direction_6,direction_max_ratio]+[direction_dict['max'], direction_dict['min'], direction_dict['arg'], direction_dict['median'],direction_dict['more'][0], direction_dict['std'], direction_dict['sum'], direction_dict['mad'], direction_var]
            csv_name = ['direction_12','direction_max_ratio','direction_ratio_max', 'direction_ratio_min', 'direction_ratio_arg', 'direction_ratio_median',
                        'direction_ratio_more', 'direction_ratio_std', 'direction_ratio_sum', 'direction_ratio_mad', 'direction_ratio_var']
            out_list += [add]
            #print(i)
    write_csv(csv_name, out_list, csv_N)


if __name__ == '__main__':
    feature_hour("train")
    feature_hour("test")
    #feature_direction("train")
    #feature_direction("test")