import subprocess

subprocess.run(["pip","install","numpy"])


import numpy as np
from collections import Counter

# 训练数据：每部电影表示为 [打斗镜头次数, 接吻镜头次数, 类别]
# 类别：'动作片' 或 '爱情片'
train_data = [
    [5, 100, '爱情片'],
    [7, 95, '爱情片'],
    [2, 88, '爱情片'],
    [90, 10, '动作片'],
    [88, 5, '动作片'],
    [95, 3, '动作片'],
    [15, 80, '爱情片'],
    [85, 8, '动作片']
]

# 新电影特征
new_movie = [10, 90]

# k值
k = 3

# 提取特征和标签
X_train = np.array([item[:2] for item in train_data])
y_train = np.array([item[2] for item in train_data])

s=[1,2]
# print(f"s:{type(s)}")
print(type(y_train))

print(f"{y_train}")
# 计算欧氏距离
distances = np.sqrt(np.sum((X_train - new_movie) ** 2, axis=1))

# 获取距离最小的k个邻居的索引
k_nearest_indices = distances.argsort()[:k]

# 获取这k个邻居的类别
k_nearest_labels = y_train[k_nearest_indices]

# 投票决定类别（多数表决）
predicted_label = Counter(k_nearest_labels).most_common(1)[0][0]

print(f"新电影（打斗: {new_movie[0]}, 接吻: {new_movie[1]}）被预测为：{predicted_label}")