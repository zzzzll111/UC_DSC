import pandas as pd
import matplotlib.pyplot as plt

# 读取 Excel 文件
file_path = '../EXP.xlsx'
data = pd.read_excel(file_path)

# 计算百分比
data['Percentage'] = data['number'] / data['total'] * 100

# 创建图表和两个纵坐标轴
fig, ax1 = plt.subplots(figsize=(12, 8))

# 绘制第一个纵坐标轴数据（Number of Selected Points）
ax1.set_xlabel('Privacy Level (n)')
ax1.set_ylabel('Number of Selected Points', color='tab:blue')
line1, = ax1.plot(data['level'], data['number'], color='tab:blue', marker='o', label='Number of Selected Points')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# 创建第二个纵坐标轴
ax2 = ax1.twinx()
ax2.set_ylabel('Percentage (%)', color='tab:orange')
line2, = ax2.plot(data['level'], data['Percentage'], color='tab:orange', marker='x', linestyle='--', label='Percentage')
ax2.tick_params(axis='y', labelcolor='tab:orange')

# 添加图例
fig.tight_layout()
fig.legend(loc='upper right', bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)

# 添加标注
for i in range(len(data)):
    level = data['level'].iloc[i]
    number = data['number'].iloc[i]
    percentage = data['Percentage'].iloc[i]

    # 标注 Number of Selected Points
    ax1.annotate(f'{number}',
                  (level, number),
                  textcoords="offset points",
                  xytext=(5,5),
                  ha='center',
                  color='tab:blue')

    # 标注 Percentage
    ax2.annotate(f'{percentage:.2f}%',
                  (level, percentage),
                  textcoords="offset points",
                  xytext=(5,-10),
                  ha='center',
                  color='tab:orange')

# 保存图形到 PDF 文件
plt.grid(True)
plt.savefig('1.pdf', format='pdf', bbox_inches='tight')  # 保存为 PDF 文件，并去除多余空白
plt.close()  # 关闭图形以释放资源
