智能算法赛：智慧海洋建设https://tianchi.aliyun.com/competition/entrance/231768/information
比赛止步于复赛，相比与前排还是很多经验不足，分享下我们的方案，坐等学习大佬方案。

模型思路：
在特征方面：
  本次比赛我们分别在清洗前的数据和清洗后的数据中提取了相关特征。在清洗前的数据提取了坐标x，y，速度v，角加速度w的基本统计量，分别用了9个，并对其中去除了个别不大合理的已简化模型。对原始数据进行清洗，同一规则下清洗5次，去除异常值（如坐标的偏移，异常的速度和方向值等），然后在清洗后的数据中提取关于作业时间的数据如开始作业，运行次数，时间占比等（最后选用了4个）。
在模型方面：
  用了xgboost，参数见xgb_train.py,40折获得最后的提交结果。

环境
python 3.6
pandas
numpy
xgboost
sklearn
shutil

加载说明(提取特征到生成提交文件要大概35分钟左右):
1、将解压后的数据放置在data/下。
2、运行main.py。
3、生成的result.csv保存在根目录下。

