import openpyxl
import matplotlib.pyplot as plt

# 加载 Excel 文件
file_path = 'blockchain.xlsx'
wb = openpyxl.load_workbook(file_path)

# 选择名为 '9' 的工作表
sheet = wb['9']

# 提取数据
x_points = [0, 50, 100, 150, 200, 250, 300]
data = [sheet[f'B{row}'].value for row in range(2, 9)]

# 绘制图表
plt.figure(figsize=(10, 6))

plt.plot(x_points, data, marker='o', color='blue', label='Data')

# 设置x轴和y轴标签
plt.xlabel('Time Of Experiments')
plt.ylabel('Time Cost/ms')

# 设置y轴范围
plt.ylim(10, 25)

plt.legend()
plt.grid(True)

# 保存图表为 PDF 文件
plt.savefig('9.pdf', format='pdf')

# 显示图表
plt.show()

print("图表已保存为 9.pdf")
