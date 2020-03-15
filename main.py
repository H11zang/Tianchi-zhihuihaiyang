import os
from extract_feature_2nd import feature_hour,feature_direction
from pretreatment import pretreatment
from extract_feature_Fclean import feature_clean
from extract_feature import feature
from result_online import result
from evaluate import evaluate
from xgb_train import model_set

def make_feature(state,root):
    if state == 'train':
        feature("train",root)
        feature_clean("train", root)
        #pretreatment("train", 5,root)
        feature_hour("train")
        feature_direction("train")
    if state == 'test':
        feature("test",root)
        #pretreatment("test", 5,root)
        feature_clean("test",root)
        feature_hour("test")
        feature_direction("test")

if __name__ == '__main__':
    #创建文件夹
    if not os.path.exists("dataset_train/"):
        os.mkdir("dataset_train/")
    if not os.path.exists("dataset_test/"):
        os.mkdir("dataset_test/")
    if not os.path.exists("test_pretreatment/"):
        os.mkdir("test_pretreatment/")
    if not os.path.exists("test_pretreatment2/"):
        os.mkdir("test_pretreatment2/")
    if not os.path.exists("train_pretreatment/"):
        os.mkdir("train_pretreatment/")
    if not os.path.exists("train_pretreatment2/"):
        os.mkdir("train_pretreatment2/")
    if not os.path.exists("result/"):
        os.mkdir("result/")
    if not os.path.exists("model/"):
        os.mkdir("model/")
    train_root = '/tcdata/hy_round2_train_20200225'
    test_root = '/tcdata/hy_round2_testB_20200312'
    #train_root = 'C:/Users/zang/Desktop/智慧海洋建设/data/hy_round2_train_20200225'
    #test_root = 'C:/Users/zang/Desktop/智慧海洋建设/data/hy_round1_testB_20200221'
    #提取特征
    make_feature('train',train_root)
    make_feature('test',test_root)
    #训练
    speed_name = ['speed_min','speed_arg','speed_median','speed_more','speed_std','speed_sum','speed_mad','speed_var']
    x_name = ['x_max','x_min','x_arg','x_median','x_more','x_sum','x_mad','x_var']
    y_name = ['y_max','y_min','y_arg','y_median','y_more','y_sum','y_mad','y_var']
    w_name = ['w_max','w_min','w_arg','w_median','w_more','w_sum','w_std','w_mad','w_var']
    work_time_name = ['work_time_max', 'work_time_min', 'work_time_arg', 'work_time_median', 'work_time_more','work_time_std', 'work_time_sum', 'work_time_mad', 'work_time_var']
    direction_name = ['direction_max_ratio', 'direction_ratio_max', 'direction_ratio_min',
                'direction_ratio_arg', 'direction_ratio_median',
                'direction_ratio_more', 'direction_ratio_std', 'direction_ratio_sum', 'direction_ratio_mad',
                'direction_ratio_var']
    others_name = ['fisher_time','area']
    drop_out = ['speed_max','0~6','7~12','13~18','19~23','x_std','y_std']+work_time_name+direction_name+['0T5_vs_13T18', '8T12_vs_19t23', '13T18_vs_19t23']#0.9024 600 0.9044
    drop_out_test = speed_name + x_name + y_name + w_name + others_name + ['direction_12', '0T5_vs_8T12', '8T12_vs_13T18','0T5_vs_19t23','ratio_9t22']
    model_set('_1.11',drop_out,0)
    #生成提交文件
    result(drop_out)
    #evaluate()