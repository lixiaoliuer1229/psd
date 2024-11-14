import numpy as np
import pandas as pd

p=1/2
print(-((p*np.log2(p))+(p*np.log2(p))))

row_data = {'是否陪伴' :[0,0,0,1,1],'是否玩游戏':[1,1,0,1,1],
'渣男' :['是','是','不是','不是','不是']}
dataSet = pd.DataFrame(row_data)
print(dataSet)

def calEnt(dataSet):
    n = dataSet.shape[0] # 数据集总行数
    iset = dataSet.iloc[:,
    -1].value_counts() # 标签的所有类别
    p = iset/n # 每一类标签所占比
    ent = (-p*np.log2(p)).sum() # 计算信息熵
    return ent

result = calEnt(dataSet)
print(result)