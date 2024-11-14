import pandas as pd
import numpy as np

data = [[-1,2],[-0.5,6],[0,10],[1,18]]
data=pd.DataFrame(data)
result = (data-np.min(data,axis=0))/(np.max(data,axis=0)-np.min(data,axis=0))
# print(result)


from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

# 读取数据集
data = load_breast_cancer()

# DateFrame格式显示
X = data.data
y = data.target

from sklearn.preprocessing import MinMaxScaler as mms
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score as CVS
import matplotlib.pyplot as plt

Xtrain,Xtest,Ytrain,Ytest=train_test_split(X,y,test_size=0.2,random_state=420)
#归一化
MMS_01=mms().fit(Xtrain) #求训练集最大/小值
MMS_02=mms().fit(Xtest) #求测试集最大/小值

#转换
X_train=MMS_01.transform(Xtrain)
X_test =MMS_02.transform(Xtest)
print(X_train)
print(X_test)
score=[]
var=[]
krange=range(1,20) #设置不同的k值，从1到19都看看
for i in krange:
    clf=KNeighborsClassifier(n_neighbors=i)
    cvresult=CVS(clf,X_train,Ytrain,cv=5) # 交叉验证的每次得分
    score.append(cvresult.mean())
    var.append(cvresult.var())

plt.plot(krange,score,color="k")
plt.plot(krange,np.array(score)+np.array(var)*2,c='red',linestyle='--')
plt.plot(krange,np.array(score)-np.array(var)*2,c='red',linestyle='--')
# plt.show()

clf=KNeighborsClassifier(n_neighbors=6,weights='distance').fit(X_train,Ytrain)
score=clf.score(X_test,Ytest)
print(score)

