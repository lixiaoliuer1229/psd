from sklearn.neighbors import KNeighborsClassifier
import pandas as pd

rowdata = {'颜色深度':
[14.13,13.2,13.16,14.27,13.24,12.07,12.43,11.79,12.37,12.04],
'酒精浓度': [5.64,4.28,5.68,4.80,4.22,2.76,3.94,3.1,2.12,2.6],
'品种': [0,0,0,0,0,1,1,1,1,1]}
# 0 代表 “黑皮诺”，1 代表 “赤霞珠”
wine_data = pd.DataFrame(rowdata)

print(wine_data)

# 0 代表 “黑皮诺”，1 代表 “赤霞珠”
clf = KNeighborsClassifier(n_neighbors = 3)
clf = clf.fit(wine_data.iloc[:,0:2], wine_data.iloc[:,-1])


new_data = pd.DataFrame([[12.8, 4.1]], columns=["颜色深度", "酒精浓度"])
print(new_data)

result = clf.predict(new_data)# 返回预测的标签
print(result)

score = clf.score(new_data,[0])
print(score)