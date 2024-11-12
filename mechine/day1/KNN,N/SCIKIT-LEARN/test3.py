"""
带交叉验证的学习曲线
"""
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score as CVS

# 读取数据集
data = load_breast_cancer()

# DateFrame格式显示
X = data.data
y = data.target

name = ['平均半径','平均纹理','平均周长','平均面积',
        '平均光滑度','平均紧凑度','平均凹度',
        '平均凹点','平均对称','平均分形维数',
        '半径误差','纹理误差','周长误差','面积误差',
        '平滑度误差','紧凑度误差','凹度误差',
        '凹点误差','对称误差',
        '分形维数误差','最差半径','最差纹理',
        '最差的边界','最差的区域','最差的平滑度',
        '最差的紧凑性','最差的凹陷','最差的凹点',
        '最差的对称性','最差的分形维数','患病否']

data=np.concatenate((X,y.reshape(-1,1)),axis=1)
table=pd.DataFrame(data=data,columns=name)
table.head()

Xtrain,Xtest,Ytrain,Ytest = train_test_split(X,y,test_size=0.2,random_state=420)
clf = KNeighborsClassifier(n_neighbors=8)
cvresult = CVS(clf,Xtrain,Ytrain,cv=6) #训练集对折6次，一共6个预测率输出
print(cvresult)

# 均值：查看模型的平均效果
print(cvresult.mean())

# 方差：查看模型是否稳定
print(cvresult.var())


score = []
var = []
krange=range(1,20) #设置不同的k值，从1到19都看看
for i in krange:
        clf = KNeighborsClassifier(n_neighbors=i)
        cvresult = CVS(clf,Xtrain,Ytrain,cv=5)
        score.append(cvresult.mean()) # 每次交叉验证返回的得分数组，再求数组均值
        var.append(cvresult.var())


import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False
# 解决中文乱码问题
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 或者 'PingFang SC'plt.style.use('ggplot')
print(krange)
plt.plot(krange,score,color='k')
plt.plot(krange,np.array(score)+np.array(var)*2,c='red',linestyle='--')
plt.plot(krange,np.array(score)-np.array(var)*2,c='red',linestyle='--')
plt.show()