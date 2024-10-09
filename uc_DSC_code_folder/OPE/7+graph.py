import openpyxl
import matplotlib.pyplot as plt

# 使用系统默认字体
plt.rcParams['font.family'] = 'sans-serif'

# 加载 Excel 文件
file_path = 'blockchain.xlsx'
wb = openpyxl.load_workbook(file_path)

# 选择名为 '7' 的工作表
sheet = wb['7']

# 提取数据
time_points = [0, 5, 10, 15, 20, 25, 30]
labels = ['P-192', 'P-224', 'P-256', 'P-384', 'P-521']
data = {label: [] for label in labels}

# 从工作表中读取数据
for i, label in enumerate(labels):
    start_row = 2 + i * 7
    end_row = start_row + 7
    data[label] = [float(sheet[f'B{row}'].value) if sheet[f'B{row}'].value is not None else 0 for row in range(start_row, end_row)]

# 绘制图表
plt.figure(figsize=(10, 6))

for label in labels:
    plt.plot(time_points, data[label], marker='o', label=label)

plt.xlabel('Time Of Experiments')
plt.ylabel('Time Cost/ms')
plt.ylim(0, 25)  # 设置 y 轴最大值
plt.legend()
plt.grid(True)

# 保存图表为 PDF 文件
plt.savefig('7.pdf', format='pdf')

# 显示图形
plt.show()

print("图表已保存为 7.pdf")
