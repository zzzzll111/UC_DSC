import pandas as pd
import matplotlib.pyplot as plt

# 定义文件路径和插入数目
base_path = 'exp/10/'
file_names = ['5000.xlsx', '10000.xlsx', '15000.xlsx', '20000.xlsx', '25000.xlsx', '30000.xlsx', '35000.xlsx', '40000.xlsx']
insert_numbers = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000]

# 存储数据
total_costs = []
average_costs = []
normalized_cost_per_item = []

for file_name in file_names:
    file_path = base_path + file_name
    try:
        # 读取Excel文件
        xls = pd.ExcelFile(file_path)

        # 读取第一页和第二页的“总开销”
        df1 = pd.read_excel(xls, sheet_name=0)
        df2 = pd.read_excel(xls, sheet_name=1)

        # 获取总开销
        total_cost1 = df1[df1.iloc[:, 0] == '总开销'].iloc[0, 1]
        total_cost2 = df2[df2.iloc[:, 0] == '总开销'].iloc[0, 1]
        total_cost = total_cost1 + total_cost2

        # 读取第三页的“平均开销”
        df3 = pd.read_excel(xls, sheet_name=2)
        average_cost = df3[df3.iloc[:, 0] == '平均开销'].iloc[0, 1]

        # 计算每项的标准化总开销
        normalized_cost_per_item.append(total_cost / insert_numbers[file_names.index(file_name)])

        # 添加到列表
        total_costs.append(total_cost)
        average_costs.append(average_cost)
        # 这里的 normalized_total_costs 不再需要
        # normalized_total_costs.append(total_cost / insert_numbers[file_names.index(file_name)])

    except Exception as e:
        print(f"Error processing {file_name}: {e}")



# 绘图
fig, ax1 = plt.subplots(figsize=(12, 8))

# 曲线1: Total Insert Cost
color = 'tab:blue'
ax1.set_xlabel('Number of Inserted Items')
ax1.set_ylabel('Total Insert Cost', color=color)
ax1.plot(insert_numbers, total_costs, marker='o', linestyle='-', color=color, label='Total Insert Cost')
ax1.tick_params(axis='y', labelcolor=color)

# 创建第二个 Y 轴共享 X 轴
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Average Lookup Cost / Average Insert Cost', color=color)
ax2.plot(insert_numbers, average_costs, marker='s', linestyle='--', color=color, label='Average Lookup Cost')
ax2.plot(insert_numbers, normalized_cost_per_item, marker='x', linestyle=':', color='tab:orange', label='Average Insert Cost')
ax2.set_ylim(0.00015, 0.007)  # 设置 y 轴范围
ax2.tick_params(axis='y', labelcolor=color)

# 添加图例
fig.tight_layout()  # 自动调整布局以避免重叠
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# 显示网格
ax1.grid(True)

# 保存图形为 PDF 文件
plt.savefig('10.pdf')

# 显示图形
plt.show()
