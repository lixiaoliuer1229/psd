#全部行都能输出
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity ="all"
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 解决坐标轴刻度负号乱码
plt.rcParams['axes.unicode_minus'] = False
# 解决中文乱码问题
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 或者 'PingFang SC'plt.style.use('ggplot')

rowdata = {'颜色深度':
[14.13,13.2,13.16,14.27,13.24,12.07,12.43,11.79,12.37,12.04],
'酒精浓度': [5.64,4.28,5.68,4.80,4.22,2.76,3.94,3.1,2.12,2.6],
'品种': [0,0,0,0,0,1,1,1,1,1]}
# 0 代表 “黑皮诺”，1 代表 “赤霞珠”
wine_data = pd.DataFrame(rowdata)

X = np.array(wine_data.iloc[:,0:2]) #我们把特征（酒的属性）放在X
y = np.array(wine_data.iloc[:,-1]) #把标签（酒的类别）放在Y
print(y)

new_data = np.array([12.03,4.1])

# y相当于做了X的索引
plt.scatter(X[y==1,0], X[y==1,1], color='red', label = '赤珠霞')
plt.scatter(X[y==0,0], X[y==0,1], color='purple', label = '黑皮诺')

plt.scatter(new_data[0],new_data[1], color='yellow')

plt.xlabel('酒精浓度')
plt.ylabel('颜色深度')
plt.legend(loc='lower right')
# plt.show()

from math import sqrt
distance = [sqrt(np.sum((x-new_data)**2)) for x in X ]
print(distance)

# 返回排序后的索引
sort_dist = np.argsort(distance)
print(sort_dist)

k = 3
topK = [y[i] for i in sort_dist[:k]]
print(topK)