import pandas as pd
import matplotlib.pyplot as plt

# 读取Excel文件中的数据
file_path = '2.xlsx'
df = pd.read_excel(file_path, sheet_name=0, usecols="B:C", skiprows=1, nrows=30)

# 计算第一条曲线前0、5、15、20、25、30行数据的总和
cumulative_sums_curve1 = [df.iloc[:i, 0].sum() for i in [0, 5, 15, 20, 25, 30]]

# 计算第二条曲线前0、5、15、20、25、30行数据的总和
cumulative_sums_curve2 = [df.iloc[:i, 1].sum() for i in [0, 5, 15, 20, 25, 30]]

# 定义Time Of Experiments
experiments = [0, 5, 15, 20, 25, 30]

# 创建一个图形对象并定义尺寸
fig, ax1 = plt.subplots(figsize=(10, 6))

# 绘制曲线1，使用左侧纵坐标轴
color1 = 'blue'
ax1.set_xlabel('Time Of Experiments')
ax1.set_ylabel('Computation Cost (s) - Workers', color=color1)
line1, = ax1.plot(experiments, cumulative_sums_curve1, marker='o', linestyle='-', color=color1, label='Workers')
ax1.tick_params(axis='y', labelcolor=color1)

# 添加曲线1的数据点标签
for i, txt in enumerate(cumulative_sums_curve1):
    ax1.annotate(f'{txt:.2f}', (experiments[i], cumulative_sums_curve1[i]), textcoords="offset points", xytext=(0,5), ha='center')

# 获取左侧坐标轴数据的最大值，并适当增加范围
max_curve1 = max(cumulative_sums_curve1)
ax1.set_ylim(0, max_curve1 * 1.1)  # 将最大值设置为数据最大值的1.1倍

# 创建第二个纵坐标轴，共享相同的横坐标轴
ax2 = ax1.twinx()
color2 = 'red'
ax2.set_ylabel('Computation Cost (s) - Requester', color=color2)
line2, = ax2.plot(experiments, cumulative_sums_curve2, marker='s', linestyle='--', color=color2, label='Requester')
ax2.tick_params(axis='y', labelcolor=color2)

# 添加曲线2的数据点标签
for i, txt in enumerate(cumulative_sums_curve2):
    ax2.annotate(f'{txt:.2f}', (experiments[i], cumulative_sums_curve2[i]), textcoords="offset points", xytext=(0,5), ha='center')

# 设置右侧坐标轴的范围
ax2.set_ylim(0, 0.6)  # 固定最大值为0.6

# 添加图例
lines = [line1, line2]
labels = ['Workers', 'Requester']
fig.legend(lines, labels, loc='upper left', bbox_to_anchor=(0.1,0.9))

# 保存图形为PDF文件
plt.savefig('2.pdf', format='pdf')

# 调整图形布局
fig.tight_layout()  # 确保标签不重叠
plt.grid(True)
plt.show()
