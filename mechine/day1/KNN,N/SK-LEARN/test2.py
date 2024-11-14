from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

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
# print(table.head())

# 划分训练集和测试集 #30%数据作为训练集
Xtrain,Xtest,Ytrain,Ytest = train_test_split(X,y,test_size=0.2,random_state=420)
# 建立模型&评估模型
clf = KNeighborsClassifier(n_neighbors=4)
# 建立分类器
clf = clf.fit(Xtrain,Ytrain)
score = clf.score(Xtest,Ytest)
print(score)

# 如何用上面分类器拟合结果找出离 Xtest 中第 20 行和第 30 行最近的 4 个“点”?
result = clf.kneighbors(Xtest[[20,30],:],return_distance=True)
print(result)


clf = KNeighborsClassifier(n_neighbors=7)
# 建立分类器
clf = clf.fit(Xtrain,Ytrain)
score = clf.score(Xtest,Ytest)
print(score)


import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False
# 解决中文乱码问题
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 或者 'PingFang SC'plt.style.use('ggplot')

score = [ ]
krange = range(1,20)
for i in krange:
        clf = KNeighborsClassifier(n_neighbors=i)
        clf = clf.fit(Xtrain,Ytrain)
        score.append(clf.score(Xtest,Ytest))
plt.plot(krange,score)
# plt.show()

max_index = score.index(max(score))+1
print(max_index)