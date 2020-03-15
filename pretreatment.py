import csv
import pandas as pd
import os
import numpy as np

#历遍文件夹
def findcsv(path, ret):
    #print('开始遍历文件夹')
    n = 0
    filelist = os.listdir(path)
    for filename in filelist:
        de_path = os.path.join(path, filename)
        n = n+1
        #print(n)
        if os.path.isfile(de_path):
            if de_path.endswith(".csv"):
                ret.append(de_path)
        else:
            findcsv(de_path, ret)

#输出csv文件
def write_csv(list,csv_N):
    test = pd.DataFrame(data=list)
    test.to_csv(csv_N, encoding='gbk', index=None,header=None)

def xy_change_state(list,n1,n2,state):
    if state >= 2 or n1 == 1:
        return False
    if list[n1-1][1] == list[n1][1] and list[n1-1][2] == list[n1][2]:
        return xy_change_state(list, n1-1, n2, state+1)
    elif list[n1-1][1] == list[n2][1] and list[n1-1][2] == list[n2][2]:
        return True
    else:
        return False

def pretreatment(state,time,root):
    for j in range(time):
        differ_num = 0
        if state == "train":
            root = [root,'train_pretreatment','train_pretreatment2']
        if state == "test":
            root = [root, 'test_pretreatment', 'test_pretreatment2']
        label_name = ['拖网', '围网', '刺网']  # 拖网、围网、刺网
        ret = []
        num = 0
        if j == 0:
            in_root = root[0]
        else:
            in_root = root[2-int(j%2)]
        findcsv(in_root, ret)
        for path in ret:
            num += 1
            with open(path) as f:
                reader = csv.reader(f)
                reader_list = list(reader)
                pretreatment_result = [reader_list[0],reader_list[1]]
                for i in range(1,len(reader_list)):
                    data_1 = reader_list[i][5].split(" ")
                    hour_1 = data_1[1].split(":")
                    all_minute1 = float(hour_1[0]) * 60 + float(hour_1[1])
                    data_2 = pretreatment_result[len(pretreatment_result)-1][5].split(" ")
                    hour_2 = data_2[1].split(":")
                    all_minute2 = float(hour_2[0]) * 60 + float(hour_2[1])
                    v_zero_state = 0
                    if abs(all_minute2-all_minute1) >= 8:
                        if i < len(reader_list)-1 and i > 1:
                            if reader_list[i][1] != reader_list[i + 1][1] and reader_list[i][2] != reader_list[i + 1][2]:
                                if xy_change_state(reader_list,i,i+1,0):
                                    reader_list[i][1] = reader_list[i+1][1]
                                    reader_list[i][2] = reader_list[i+1][2]

                            if float(reader_list[i][1]) == float(reader_list[i+1][1]) and float(reader_list[i][2]) == float(reader_list[i+1][2]):
                                v_zero_state = 1
                            if float(reader_list[i-1][3]) == 0 and float(reader_list[i+1][3]) == 0:
                                v_zero_state = 1
                            if float(reader_list[i - 1][4]) == 0 and float(reader_list[i + 1][4]) == 0:
                                v_zero_state = 1
                            if v_zero_state == 1:
                                if state == "train":
                                    pretreatment_result += [[reader_list[i][0],reader_list[i][1],reader_list[i][2],0,0,reader_list[i][5],reader_list[i][6]]]
                                    differ_num += 1
                                if state == "test":
                                    pretreatment_result += [[reader_list[i][0],reader_list[i][1],reader_list[i][2],0,0,reader_list[i][5]]]
                                    differ_num += 1
                            else:
                                pretreatment_result += [reader_list[i]]
                        elif i == len(reader_list) - 1:
                            if reader_list[i][1] == reader_list[i-1][1] and reader_list[i][2] == reader_list[i-1][2]:
                                if state == "train":
                                    pretreatment_result += [[reader_list[i][0], reader_list[i][1], reader_list[i][2], 0, 0, reader_list[i][5],reader_list[i][6]]]
                                    differ_num += 1
                                if state == "test":
                                    pretreatment_result += [[reader_list[i][0], reader_list[i][1], reader_list[i][2], 0, 0, reader_list[i][5]]]
                                    differ_num += 1
                            else:
                                pretreatment_result += [reader_list[i]]

            #print("当前进度：",num)
            out_root = root[int(j%2)+1]+'/'
            write_csv(pretreatment_result, out_root+str(path.split("\\")[1]))
        #print("finish!",differ_num)

if __name__ == '__main__':
    pretreatment("train",4)
    pretreatment("test",4)