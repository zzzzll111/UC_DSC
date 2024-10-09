import matplotlib.pyplot as plt

# 定义数据
workers = [0, 500, 1000, 1500, 2000, 2500, 3000]
single_proving_key = 4382834920  # bit
single_proof = 6804  # bit
single_verify_key = 6072  # bit

# 计算不同worker数量下的值
proving_key_gb = [single_proving_key * w / 8 / 1024 / 1024 / 1024 for w in workers]  # 转换为GB
proof_kb = [single_proof * w / 8 / 1024 for w in workers]  # 转换为KB
verify_key_kb = [single_verify_key * w / 8 / 1024 for w in workers]  # 转换为KB

# 打印调试信息
print("Proving Key (GB):", proving_key_gb)
print("Proof (KB):", proof_kb)
print("Verify Key (KB):", verify_key_kb)

# 创建图表
fig, ax1 = plt.subplots(figsize=(12, 6))

# 左边y轴 - 较小的数据
ax1.set_xlabel('Number Of Workers')
ax1.set_ylabel('Size (KB)', color='red')

# 使用不同的标记样式
ax1.plot(workers, proof_kb, label='Proof', marker='o', color='red')
ax1.plot(workers, verify_key_kb, label='Verify Key', marker='s', color='red')
ax1.tick_params(axis='y', labelcolor='red')

# 调整左侧y轴的范围，以便清楚显示 proof 曲线
ax1.set_ylim(0, max(proof_kb) * 3)  # 将y轴上限设置为proof最大值的3倍

# 为每个数据点添加数值标签和单位
for i, txt in enumerate(proof_kb):
    ax1.annotate(f'{txt:.2f} KB', (workers[i], proof_kb[i]), textcoords="offset points", xytext=(0,10), ha='center', color='red')
for i, txt in enumerate(verify_key_kb):
    ax1.annotate(f'{txt:.2f} KB', (workers[i], verify_key_kb[i]), textcoords="offset points", xytext=(0,-20), ha='center', color='red')

# 右边y轴 - 较大的proving key数据
ax2 = ax1.twinx()
ax2.set_ylabel('Size (GB)', color='blue')
ax2.plot(workers, proving_key_gb, label='Prove Key', marker='o', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

# 固定右侧y轴的范围和刻度
max_proving_key_gb = max(proving_key_gb)
ax2.set_ylim(0, max_proving_key_gb * 1.2)  # 上限为最大值的1.2倍
ax2.set_yticks([0, 300, 600, 900, 1200, 1500, 1800])  # 设置合理的刻度

# 为每个数据点添加数值标签和单位
for i, txt in enumerate(proving_key_gb):
    ax2.annotate(f'{txt:.2f} GB', (workers[i], proving_key_gb[i]), textcoords="offset points", xytext=(0,-10), ha='center', color='blue')

# 添加图例
fig.tight_layout()  # 自动调整布局
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

# 保存为PDF
plt.savefig('10.pdf')

# 显示图表（可选）
plt.show()
