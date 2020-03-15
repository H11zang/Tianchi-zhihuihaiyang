import csv
import pandas as pd
import os
import numpy as np
import math
#历遍文件夹
def findcsv(path, ret):
    print('开始遍历文件夹')
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

def feature(state,root):
    if state == "train":
        csv_N = 'dataset_train'
        frist_name = ["id","label"]
        #root = 'data/train_pretreatment'
    if state == "test":
        csv_N = 'dataset_test'
        frist_name = ["id"]
        #root = 'data/test_pretreatment'
    label_name = ['拖网','围网','刺网'] #拖网、围网、刺网
    #label_name = ['鎷栫綉','鍥寸綉','鍒虹綉'] #拖网、围网、刺网
    ret = []
    num = 0
    speed_name = ['speed_max','speed_min','speed_arg','speed_median','speed_more','speed_std','speed_sum','speed_mad','speed_var']
    x_name = ['x_max','x_min','x_arg','x_median','x_more','x_std','x_sum','x_mad','x_var']
    y_name = ['y_max','y_min','y_arg','y_median','y_more','y_std','y_sum','y_mad','y_var']
    w_name = ['w_max','w_min','w_arg','w_median','w_more','w_std','w_sum','w_mad','w_var']
    a_name = ['a_max', 'a_min', 'a_arg', 'a_median', 'a_more', 'a_std', 'a_sum', 'a_mad', 'a_var']
    others_name = ['fisher_time','area','w_zero_ratio']
    findcsv(root, ret)
    '''
    id_list = np.zeros((len(ret), len(frist_name)))
    speed_out_list = np.zeros((len(ret), len(speed_name)))
    w_out_list = np.zeros((len(ret), len(w_name)))
    a_out_list = np.zeros((len(ret), len(a_name)))
    x_out_list = np.zeros((len(ret), len(x_name)))
    y_out_list = np.zeros((len(ret), len(y_name)))
    others_out_list = np.zeros((len(ret), len(others_name)))
    '''
    id_list = []
    speed_out_list = []
    w_out_list = []
    a_out_list = []
    x_out_list = []
    y_out_list = []
    others_out_list = []
    for path in ret:
        speed_dict = {'max': 0, 'min': 100000, 'arg': 0, 'median': 0, 'more': 0, 'std': 0, 'sum': 0, 'mad': 0}
        speed_uselist = []
        w_dict = {'max': 0, 'min': 100000, 'arg': 0, 'median': 0, 'more': 0, 'std': 0, 'sum': 0, 'mad': 0}
        w_uselist = []
        a_dict = {'max': 0, 'min': 100000, 'arg': 0, 'median': 0, 'more': 0, 'std': 0, 'sum': 0, 'mad': 0}
        a_uselist = []
        starthour_uselist = []
        stophour_uselist = []
        start_state = 0
        x_dict = {'max': 0, 'min': 1000000000, 'arg': 0, 'median': 0, 'more': 0, 'std': 0, 'sum': 0, 'mad': 0}
        y_dict = {'max': 0, 'min': 1000000000, 'arg': 0, 'median': 0, 'more': 0, 'std': 0, 'sum': 0, 'mad': 0}
        x_list = []
        y_list = []
        num += 1
        with open(path) as f:
            reader = csv.reader(f)
            reader_list = list(reader)
            for i in range(len(reader_list)-1,1,-1):
                data_1 = reader_list[i][5].split(" ")
                hour_1 = data_1[1].split(":")
                all_minute1 = float(hour_1[0]) * 60 + float(hour_1[1])
                #位置
                x_list += [float(reader_list[i][1])]
                y_list += [float(reader_list[i][2])]
                #速度
                speed_now = round(float(reader_list[i][3]),1)
                if speed_now >= 0.3 and speed_now < 31:#0.3
                    speed_uselist += [speed_now]
                #方向
                if i >= 2:
                    w_now = abs(float(reader_list[i][4])-float(reader_list[i-1][4]))
                    if w_now >180:
                        w_now = 360 - w_now
                    w_uselist += [w_now]
                    a_now = float(reader_list[i][3])-float(reader_list[i-1][3])
                    a_uselist += [a_now]
                #时间
                if (speed_now >=0.4 and float(reader_list[i][4]) != 0) and start_state == 0:
                    start_state = 1
                    starthour_uselist += [reader_list[i][5]]
                if speed_now <=0.2 and float(reader_list[i][4]) == 0 and start_state > 0:
                    start_state += 1
                if start_state == 4:
                    start_state = 0
                    stophour_uselist += [reader_list[i-3][5]]

            #速度
            v_df = pd.DataFrame(speed_uselist)
            if len(speed_uselist) != 0:
                v_D = v_df.describe()
                speed_dict['max'] = v_D.values[7][0]
                speed_dict['min'] = v_D.values[3][0]
                speed_dict['arg'] = v_D.values[1][0]
                speed_dict['median'] = v_D.values[5][0]
                speed_dict['std'] = v_D.values[2][0]
                speed_dict['more'] = v_df.mode().values[0][0]
                speed_dict['sum'] = v_df.sum().values[0]
                speed_dict['mad'] = v_df.mad().values[0]
            if speed_dict['min'] == 100000:
                speed_dict['min'] = 0
            speed_var = 0
            if speed_dict['arg'] != 0:
                speed_var = speed_dict['std']/speed_dict['arg']

            # 方向
            w_df = pd.DataFrame(w_uselist)
            if len(w_uselist) != 0:
                w_D = w_df.describe()
                w_dict['max'] = w_D.values[7][0]
                w_dict['min'] = w_D.values[3][0]
                w_dict['arg'] = w_D.values[1][0]
                w_dict['median'] = w_D.values[5][0]
                w_dict['std'] = w_D.values[2][0]
                w_dict['more'] = w_df.mode().values[0][0]
                w_dict['sum'] = w_df.sum().values[0]
                w_dict['mad'] = w_df.mad().values[0]
            if w_dict['min'] == 100000:
                w_dict['min'] = 0
            w_var = 0
            if w_dict['arg'] != 0:
                w_var = w_dict['std'] / w_dict['arg']

            # 加速度
            a_df = pd.DataFrame(a_uselist)
            if len(a_uselist) != 0:
                a_D = a_df.describe()
                a_dict['max'] = a_D.values[7][0]
                a_dict['min'] = a_D.values[3][0]
                a_dict['arg'] = a_D.values[1][0]
                a_dict['median'] = a_D.values[5][0]
                a_dict['std'] = a_D.values[2][0]
                a_dict['more'] = a_df.mode().values[0][0]
                a_dict['sum'] = a_df.sum().values[0]
                a_dict['mad'] = a_df.mad().values[0]
            if a_dict['min'] == 100000:
                a_dict['min'] = 0
            a_var = 0
            if a_dict['arg'] != 0:
                a_var = a_dict['std'] / a_dict['arg']


            x_df = pd.DataFrame(x_list)
            if len(x_list) != 0:
                x_D = x_df.describe()
                x_dict['max'] = x_D.values[7][0]
                x_dict['min'] = x_D.values[3][0]
                x_dict['arg'] = x_D.values[1][0]
                x_dict['median'] = x_D.values[5][0]
                x_dict['std'] = x_D.values[2][0]
                x_dict['more'] = x_df.mode().values[0][0]
                x_dict['sum'] = x_df.sum().values[0]
                x_dict['mad'] = x_df.mad().values[0]
            x_var = 0
            if x_dict['arg'] != 0:
                x_var = x_dict['std'] / x_dict['arg']

            y_df = pd.DataFrame(y_list)
            if len(y_list) != 0:
                y_D = y_df.describe()
                y_dict['max'] = y_D.values[7][0]
                y_dict['min'] = y_D.values[3][0]
                y_dict['arg'] = y_D.values[1][0]
                y_dict['median'] = y_D.values[5][0]
                y_dict['std'] = y_D.values[2][0]
                y_dict['more'] = y_df.mode().values[0][0]
                y_dict['sum'] = y_df.sum().values[0]
                y_dict['mad'] = y_df.mad().values[0]
            y_var = 0
            if y_dict['arg'] != 0:
                y_var = y_dict['std'] / y_dict['arg']

            area = (x_dict['max']-x_dict['min'])*(y_dict['max']-y_dict['min'])
            fisher_time = len(starthour_uselist)
            w_zero_ratio = w_uselist.count(0)/len(w_uselist)


            if state == "train":
                id_list += [[reader_list[2][0],label_name.index(reader_list[2][6])]]
            if state == "test":
                id_list += [[reader_list[2][0]]]
            speed_out_list += [[speed_dict['max'],speed_dict['min'],speed_dict['arg'],speed_dict['median'],speed_dict['more'],
                          speed_dict['std'],speed_dict['sum'],speed_dict['mad'],speed_var]]
            w_out_list += [[w_dict['max'], w_dict['min'], w_dict['arg'], w_dict['median'], w_dict['more'],w_dict['std'], w_dict['sum'], w_dict['mad'],w_var]]
            a_out_list += [[a_dict['max'], a_dict['min'], a_dict['arg'], a_dict['median'], a_dict['more'],a_dict['std'], a_dict['sum'], a_dict['mad'], a_var]]
            x_out_list += [[x_dict['max'],x_dict['min'],x_dict['arg'],x_dict['median'],x_dict['more'],x_dict['std'],x_dict['sum'],x_dict['mad'],x_var]]
            y_out_list += [[y_dict['max'],y_dict['min'],y_dict['arg'],y_dict['median'],y_dict['more'],y_dict['std'],y_dict['sum'],y_dict['mad'],y_var]]
            others_out_list += [[fisher_time,area,w_zero_ratio]]
        #print("当前进度：",num)
        #if num == 100:
        #    break

    write_csv(frist_name,id_list,csv_N+'/id.csv')
    write_csv(speed_name, speed_out_list, csv_N + '/speed.csv')
    write_csv(w_name, w_out_list, csv_N + '/w.csv')
    write_csv(a_name, a_out_list, csv_N + '/a.csv')
    write_csv(x_name, x_out_list, csv_N + '/x.csv')
    write_csv(y_name, y_out_list, csv_N + '/y.csv')
    #write_csv(others_name, others_out_list, csv_N + '/others.csv')
    print("finish!")

if __name__ == '__main__':
    feature("train")
    feature("test")