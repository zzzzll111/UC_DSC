import matplotlib.pyplot as plt
import pandas as pd

# 读取 Excel 数据
file_path = '../zk_exp.xlsx'  # Excel 文件路径
sheet_name = 0  # 第一个工作表
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 提取数据
proof_data = df.iloc[0:30, 1].reset_index(drop=True)  # B列数据
verify_data = df.iloc[0:30, 2].reset_index(drop=True)  # C列数据

# 打印数据以确认读取正确
print("Proof Data:")
print(proof_data.head(10))  # 打印前10行数据
print("\nVerify Data:")
print(verify_data.head(10))  # 打印前10行数据

# 计算前0、5、10、15、20、25、30个样本的总时间开销
def compute_cumulative_sum(data, indices):
    cumulative_sum = []
    for i in indices:
        if i > 0:
            cumulative_sum.append(data[:i].sum())
        else:
            cumulative_sum.append(0)  # 当 i 为 0 时，累积和为 0
    return cumulative_sum

# 定义横坐标
indices = [0, 5, 10, 15, 20, 25, 30]
workers = indices  # 横坐标为样本数量

# 计算累积时间
proof_cumulative = compute_cumulative_sum(proof_data, indices)
verify_cumulative = compute_cumulative_sum(verify_data, indices)

# 新数据
compared_data = [0, 159.5531181, 318.5247779, 477.715581, 636.1265182, 794.6400531, 953.637143]

# 打印计算结果以确认
print("\nCumulative Proof Time (ms):")
print(proof_cumulative)
print("\nCumulative Verify Time (ms):")
print(verify_cumulative)
print("\nCompared Data:")
print(compared_data)

# 创建图表
fig, ax1 = plt.subplots(figsize=(12, 6))

# 左侧 y 轴 - Verify 数据（毫秒）
ax1.set_xlabel('Number Of Workers')
ax1.set_ylabel('Verify Time Cost (ms)', color='red')
ax1.plot(workers, verify_cumulative, label='Verify Time Cost', marker='o', color='red')
ax1.plot(workers, compared_data, label='Compared Work', marker='o', color='red')  # 新数据
ax1.tick_params(axis='y', labelcolor='red')

# 在 Verify 数据点上添加数值（保留三位小数）
for i, (worker, cost) in enumerate(zip(workers, verify_cumulative)):
    ax1.annotate(f'{cost:.3f} ms', (worker, cost), textcoords="offset points", xytext=(0,5), ha='center', color='red')

# 在 Compared Data 数据点上添加数值（保留三位小数）
for i, (worker, cost) in enumerate(zip(workers, compared_data)):
    ax1.annotate(f'{cost:.3f} ms', (worker, cost), textcoords="offset points", xytext=(0,5), ha='center', color='red')

# 右侧 y 轴 - Proof 数据（秒）
ax2 = ax1.twinx()
ax2.set_ylabel('Proof Time Cost (s)', color='blue')
ax2.plot(workers, [p for p in proof_cumulative], label='Proof Time Cost', marker='o', color='blue')  # 将 proof 数据转换为秒
ax2.tick_params(axis='y', labelcolor='blue')

# 在 Proof 数据点上添加数值（保留三位小数）
for i, (worker, cost) in enumerate(zip(workers, proof_cumulative)):
    ax2.annotate(f'{cost:.3f} s', (worker, cost), textcoords="offset points", xytext=(0,5), ha='center', color='blue')

# 设置 y 轴范围
ax1.set_ylim(0, max(verify_cumulative + compared_data) * 1.1)  # Verify Time Cost (ms)
ax2.set_ylim(0, max(proof_cumulative) * 1.2)  # Proof Time Cost (s)

# 添加图例
fig.tight_layout()
ax1.legend(loc="upper left")  # 左侧坐标轴图例
ax2.legend(loc="upper right")  # 右侧坐标轴图例

# 保存为 PDF
plt.savefig('11.pdf')

# 显示图表（可选）
plt.show()
