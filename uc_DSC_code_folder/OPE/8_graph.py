import pandas as pd
import matplotlib.pyplot as plt

# 读取Excel文件中的数据
file_path = '8.xlsx'
df = pd.read_excel(file_path, sheet_name=0, usecols="B", skiprows=1, nrows=30)

# 计算前0、5、15、20、25、30行数据的总和
cumulative_sums = [df.iloc[:i].sum().values[0] for i in [0, 5, 15, 20, 25, 30]]

# 定义Number Of Workers
workers = [0, 5, 15, 20, 25, 30]

# 绘制折线图
plt.figure(figsize=(10, 6))
plt.plot(workers, cumulative_sums, marker='o', linestyle='-', color='b')

# 添加标签
plt.xlabel('Number Of Workers')
plt.ylabel('Computation Cost (s)')

# 显示网格
plt.grid(True)

# 为每个数据点添加数值标签
for i, txt in enumerate(cumulative_sums):
    plt.annotate(f'{txt:.2f}', (workers[i], cumulative_sums[i]), textcoords="offset points", xytext=(0,5), ha='center')


# 保存图像为PDF文件
plt.savefig('8.pdf', format='pdf')

# 显示图像
plt.show()
