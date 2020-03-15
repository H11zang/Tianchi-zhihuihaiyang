import csv
import pandas as pd
import os
import numpy as np
from extract_feature_2nd import feature_hour
from pretreatment import pretreatment


def count_out(input_list):
    d_df = pd.DataFrame(input_list)
    d_D = d_df.describe()
    max = d_D.values[7][0]
    min = d_D.values[3][0]
    arg = d_D.values[1][0]
    median = d_D.values[5][0]
    std = d_D.values[2][0]
    more = d_df.mode().values[0][0]
    sum = d_df.sum().values[0]
    mad = d_df.mad().values[0]
    c_75 = d_D.values[6][0]
    c_25 = d_D.values[4][0]
    output = [max, min, arg, median,more, std, sum, mad, c_75, c_25]
    return output

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
def write_csv(csv_name,list,csv_N):
    test = pd.DataFrame(columns=csv_name, data=list)
    test.to_csv(csv_N, encoding='gbk', index=None)

def sum_list(list):
    sum = 0
    for i in range(len(list)):
        sum += float(list[i])
    return sum

def max_list(lt):
    temp = 0
    for i in lt:
        if lt.count(i) > temp:
            max_str = i
            temp = lt.count(i)
    return max_str

def dec_zero(w_list):
    i = 0
    start = 0
    stop =0
    while i < len(w_list):
        if i<len(w_list) and w_list[0] == 0:
            i += 1
            stop = i
        if i<len(w_list) and w_list[i] == 0 and stop == 0:
            start = i
            stop = i
        if i<len(w_list) and w_list[i] == 0 and (start != 0 or stop != 0):
            stop = i
        if i<len(w_list) and w_list[i] != 0 and (stop != 0):
            w_list = w_list[:start]+w_list[stop:]
            i = start
            start = 0
            stop = 0
        i += 1
    return w_list

def xy_change_state(list,n1,n2,state):
    if state >= 2 or n1 == 1:
        return False
    if list[n1-1][1] == list[n1][1] and list[n1-1][2] == list[n1][2]:
        return xy_change_state(list, n1-1, n2, state+1)
    elif list[n1-1][1] == list[n2][1] and list[n1-1][2] == list[n2][2]:
        return True
    else:
        return False

def feature_clean(state,root):
    if state == "train":
        csv_N = 'dataset_train'
        frist_name = ["id","label"]
        #root = 'train_pretreatment'
    if state == "test":
        csv_N = 'dataset_test'
        frist_name = ["id"]
        #root = 'test_pretreatment'
    label_name = ['拖网','围网','刺网'] #拖网、围网、刺网
    #label_name = ['鎷栫綉','鍥寸綉','鍒虹綉'] #拖网、围网、刺网
    ret = []
    num = 0
    work_time_name = ['work_time_max', 'work_time_min', 'work_time_arg', 'work_time_median', 'work_time_more', 'work_time_std', 'work_time_sum', 'work_time_mad', 'work_time_var']
    xy_name = ['xy_max', 'xy_min', 'xy_arg', 'xy_median', 'xy_more','xy_std', 'xy_sum', 'xy_mad', 'xy_75', 'xy_25']
    hour_ratio_name = ['0h','1h','2h','3h','4h','5h','6h','7h','8h','9h','10h','11h','12h','13h','14h','15h','16h','17h','18h','19h','20h','21h','22h','23h']
    direction_name = []
    for i in range(36):
        add = str(i*10)+"-"+str((i+1)*10)
        direction_name += [add]
    others_name = ['fisher_time','area','0~6','7~12','13~18','19~23','0~6_ratio','7~12_ratio','13~18_ratio','19~23_ratio']
    findcsv(root, ret)
    id_list = []
    work_time_out_list = []
    hour_ratio_out_list = []
    direction_ratio_out_list = []
    xy_out_list = []
    others_out_list = []
    for path in ret:
        starthour_uselist = []
        stophour_uselist = []
        start_state = 0
        x_dict = {'max': 0, 'min': 1000000000, 'arg': 0, 'median': 0, 'more': 0, 'std': 0, 'sum': 0, 'mad': 0}
        y_dict = {'max': 0, 'min': 1000000000, 'arg': 0, 'median': 0, 'more': 0, 'std': 0, 'sum': 0, 'mad': 0}
        x_list = []
        y_list = []
        d_list = []
        dire_list = []
        dire_index_list = []
        hour_num = [0]*24
        hour_ratio = [0]*24
        direction_num = [0]*36
        direction_ratio = [0]*36
        HL = [0]*4
        strenth_state = [0] * 4
        num += 1
        with open(path) as f:
            reader = csv.reader(f)
            reader_list = list(reader)

            for clean in range(5):
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
                                if state == "test":
                                    pretreatment_result += [[reader_list[i][0],reader_list[i][1],reader_list[i][2],0,0,reader_list[i][5]]]
                            else:
                                pretreatment_result += [reader_list[i]]
                        elif i == len(reader_list) - 1:
                            if reader_list[i][1] == reader_list[i-1][1] and reader_list[i][2] == reader_list[i-1][2]:
                                if state == "train":
                                    pretreatment_result += [[reader_list[i][0], reader_list[i][1], reader_list[i][2], 0, 0, reader_list[i][5],reader_list[i][6]]]
                                if state == "test":
                                    pretreatment_result += [[reader_list[i][0], reader_list[i][1], reader_list[i][2], 0, 0, reader_list[i][5]]]
                            else:
                                pretreatment_result += [reader_list[i]]
                reader_list = pretreatment_result

            for i in range(len(reader_list)-1,1,-1):
                data_1 = reader_list[i][5].split(" ")
                hour_1 = data_1[1].split(":")
                all_minute1 = float(hour_1[0]) * 60 + float(hour_1[1])
                #位置
                x_list += [float(reader_list[i][1])]
                y_list += [float(reader_list[i][2])]
                d_list += [(float(reader_list[i][1])**2+float(reader_list[i][2])**2)**0.5]
                #速度
                speed_now = round(float(reader_list[i][3]),1)
                direction_now = float(reader_list[i][4])
                #时间
                if (speed_now > 0.2 and float(reader_list[i][4]) != 0):
                    hour_num[int(reader_list[i][5].split(" ")[1].split(":")[0])] += 1
                    dire_list += [direction_now]
                if (speed_now >0.2 and float(reader_list[i][4]) != 0) and start_state == 0:
                    start_state = 1
                    starthour_uselist += [reader_list[i][5].split(" ")[1].split(":")]
                if speed_now <=0.2 and float(reader_list[i][4]) == 0 and start_state > 0:
                    start_state += 1
                if (speed_now >0.2 and float(reader_list[i][4]) != 0) and start_state > 1:
                    start_state = 1
                if start_state == 4:
                    start_state = 0
                    stophour_uselist += [reader_list[i+3][5].split(" ")[1].split(":")]
                    dire_index_list += [len(dire_list)]
                #方向
                if direction_now != 0:
                    direction_index = int(direction_now/10)
                    if direction_index == 36:
                        direction_index = 0
                    direction_num[direction_index] += 1

            if len(dire_index_list) != 0:
                for d_i in range(len(dire_index_list)):
                    dire_num = [0]*36
                    if d_i == 0:
                        dire_now_list = dire_list[:dire_index_list[d_i]]
                    else:
                        dire_now_list = dire_list[dire_index_list[d_i-1]:dire_index_list[d_i]]
                    for d_j in range(len(dire_now_list)):
                        direction_index = int(dire_now_list[d_j]/10)
                        if direction_index == 36:
                            direction_index = 0
                        dire_num[direction_index] += 1
                    #ratio_12 = []
                    #for j in range(12):
                    #    ratio_12 += [sum_list(dire_num[j*3:j*3+3])]
                    direction_12 = 36 - dire_num.count(0)
                    if direction_12 < 9: strenth_state[0] += 1
                    if direction_12 >= 9 and direction_12 < 18: strenth_state[1] += 1
                    if direction_12 >= 18 and direction_12 < 27: strenth_state[2] += 1
                    if direction_12 >= 27 and direction_12 <= 36: strenth_state[3] += 1

                if dire_index_list[d_i] < len(dire_list)-1:
                    dire_now_list = dire_list[dire_index_list[d_i]:]
                    for d_j in range(len(dire_now_list)):
                        direction_index = int(dire_now_list[d_j]/10)
                        if direction_index == 36:
                            direction_index = 0
                        dire_num[direction_index] += 1
                    ratio_12 = []
                    for j in range(12):
                        ratio_12 += [sum_list(dire_num[j*3:j*3+3])]
                    direction_12 = 12 - ratio_12.count(0)
                    if direction_12 < 3: strenth_state[0] += 1
                    if direction_12 >= 3 and direction_12 < 6: strenth_state[1] += 1
                    if direction_12 >= 6 and direction_12 < 9: strenth_state[2] += 1
                    if direction_12 >= 9 and direction_12 <= 12: strenth_state[3] += 1

            if len(dire_index_list) == 0 and len(dire_list) != 0:
                dire_now_list = dire_list
                for d_j in range(len(dire_now_list)):
                    direction_index = int(dire_now_list[d_j] / 10)
                    if direction_index == 36:
                        direction_index = 0
                    dire_num[direction_index] += 1
                ratio_12 = []
                for j in range(12):
                    ratio_12 += [sum_list(dire_num[j * 3:j * 3 + 3])]
                direction_12 = 12 - ratio_12.count(0)
                if direction_12 < 3: strenth_state[0] += 1
                if direction_12 >= 3 and direction_12 < 6: strenth_state[1] += 1
                if direction_12 >= 6 and direction_12 < 9: strenth_state[2] += 1
                if direction_12 >= 9 and direction_12 <= 12: strenth_state[3] += 1

            x_df = pd.DataFrame(x_list)
            if len(x_list) != 0:
                x_dict['max'] = x_df.max().values[0]
                x_dict['min'] = x_df.min().values[0]

            y_df = pd.DataFrame(y_list)
            if len(y_list) != 0:
                y_dict['max'] = y_df.max().values[0]
                y_dict['min'] = y_df.min().values[0]

            #作业时间
            work_time = []
            for i in range(len(stophour_uselist)):
                all_minute_start = float(starthour_uselist[i][0]) * 60 + float(starthour_uselist[i][1])
                all_minute_stop = float(stophour_uselist[i][0]) * 60 + float(stophour_uselist[i][1])
                if all_minute_stop < all_minute_start:
                    all_minute_stop += 1440
                work_time += [all_minute_stop-all_minute_start]
                HL_0T6_state = 0
                HL_7T12_state = 0
                HL_13T18_state = 0
                HL_19T23_state = 0
                if float(starthour_uselist[i][0]) > float(stophour_uselist[i][0]):
                    for hour in range(int(starthour_uselist[i][0]),24):
                        if hour >= 0 and hour <= 6:
                            HL_0T6_state += 1
                        if hour >= 7 and hour <= 12:
                            HL_7T12_state += 1
                        if hour >= 13 and hour <= 18:
                            HL_13T18_state += 1
                        if hour >= 19 and hour <= 23:
                            HL_19T23_state += 1
                    for hour in range(int(stophour_uselist[i][0])+1):
                        if hour >= 0 and hour <= 6:
                            HL_0T6_state += 1
                        if hour >= 7 and hour <= 12:
                            HL_7T12_state += 1
                        if hour >= 13 and hour <= 18:
                            HL_13T18_state += 1
                        if hour >= 19 and hour <= 23:
                            HL_19T23_state += 1
                else:
                    for hour in range(int(starthour_uselist[i][0]),int(stophour_uselist[i][0])+1):
                        if hour >= 0 and hour <= 6:
                            HL_0T6_state += 1
                        if hour >= 7 and hour <= 12:
                            HL_7T12_state += 1
                        if hour >= 13 and hour <= 18:
                            HL_13T18_state += 1
                        if hour >= 19 and hour <= 23:
                            HL_19T23_state += 1
                if HL_0T6_state >= 5:
                    HL[0] += 1
                if HL_7T12_state >= 5:
                    HL[1] += 1
                if HL_13T18_state >= 5:
                    HL[2] += 1
                if HL_19T23_state >= 5:
                    HL[3] += 1
            if len(work_time) == 0:
                if len(starthour_uselist) != 0:
                    all_minute_start = float(starthour_uselist[0][0]) * 60 + float(starthour_uselist[0][1])
                    stop_time = reader_list[1][5].split(" ")
                    hour_stop_time = stop_time[1].split(":")
                    all_minute_stop = float(hour_stop_time[0]) * 60 + float(hour_stop_time[1])
                    if all_minute_stop < all_minute_start:
                        all_minute_stop += 1440
                    work_time += [all_minute_stop - all_minute_start]
                else:
                    work_time = [0]

            # 运行时间
            work_time_df = pd.DataFrame(work_time)
            work_time_dict = {'max': 0, 'min': 100000, 'arg': 0, 'median': 0, 'more': 0, 'std': 0, 'sum': 0, 'mad': 0}
            if len(work_time) != 0:
                work_time_dict['max'] = work_time_df.max().values[0]
                work_time_dict['min'] = work_time_df.min().values[0]
                work_time_dict['arg'] = work_time_df.mean().values[0]
                work_time_dict['median'] = work_time_df.median().values[0]
                work_time_dict['std'] = work_time_df.std().values[0]
                work_time_dict['more'] = work_time_df.mode().values[0][0]
                work_time_dict['sum'] = work_time_df.sum().values[0]
                work_time_dict['mad'] = work_time_df.mad().values[0]
            if work_time_dict['min'] == 100000:
                work_time_dict['min'] = 0
            work_time_var = 0
            if work_time_dict['arg'] != 0:
                work_time_var = work_time_dict['std'] / work_time_dict['arg']

            hour_sum = sum(hour_num)
            if hour_sum != 0:
                for k in range(len(hour_num)):
                    hour_ratio[k] = hour_num[k]/hour_sum

            direction_sum = sum(direction_num)
            if direction_sum != 0:
                for k in range(len(direction_num)):
                    direction_ratio[k] = direction_num[k]/direction_sum

            area = (x_dict['max']-x_dict['min'])*(y_dict['max']-y_dict['min'])
            fisher_time = len(starthour_uselist)
            HL_ratio = [0]*4
            HL_sum = sum(HL)
            if HL_sum != 0:
                for HL_num in range(len(HL_ratio)):
                    HL_ratio[HL_num] = HL[HL_num]/HL_sum

            strenth_state_sum = sum(strenth_state)
            if strenth_state_sum != 0:
                for strenth_state_num in range(len(strenth_state)):
                    strenth_state[strenth_state_num] = strenth_state[strenth_state_num]/strenth_state_sum

            if state == "train":
                id_list += [[reader_list[2][0],label_name.index(reader_list[2][6])]]
            if state == "test":
                id_list += [[reader_list[2][0]]]
            work_time_out_list += [[work_time_dict['max'], work_time_dict['min'], work_time_dict['arg'], work_time_dict['median'],work_time_dict['more'], work_time_dict['std'], work_time_dict['sum'], work_time_dict['mad'], work_time_var]]
            hour_ratio_out_list += [hour_ratio]
            direction_ratio_out_list += [direction_ratio]
            others_out_list += [[fisher_time,area,HL[0],HL[1],HL[2],HL[3],HL_ratio[0],HL_ratio[1],HL_ratio[2],HL_ratio[3]]]
            if len(d_list) != 0:
                xy_out_list += [count_out(d_list)]
            if len(d_list) == 0:
                xy_out_list += [[0,0,0,0,0,0,0,0,0,0]]

        #print("当前进度：",num)
        #if num == 100:
        #    break

    write_csv(work_time_name, work_time_out_list, csv_N + '/work_time.csv')
    write_csv(hour_ratio_name, hour_ratio_out_list, csv_N + '/hour_ratio.csv')
    write_csv(direction_name, direction_ratio_out_list, csv_N + '/direction_ratio.csv')
    write_csv(xy_name, xy_out_list, csv_N + '/xy.csv')
    write_csv(others_name, others_out_list, csv_N + '/others.csv')
    #print("finish!")

if __name__ == '__main__':
    pretreatment("train",5)
    pretreatment("test",5)
    feature_clean("train")
    feature_clean("test")
    feature_hour("train")
    feature_hour("test")