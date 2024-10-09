input_file = 'pad_to_13.txt'
output_file = 'conver2int.txt'

# 打开输入文件和输出文件
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        # 分割每行的数字对
        tokens = line.strip().split()
        if len(tokens) != 2:
            continue

        # 将每个数字乘以 10^10 并取整
        num1 = int(float(tokens[0]) * 1e10)
        num2 = int(float(tokens[1]) * 1e10)

        # 将结果写入输出文件
        outfile.write(f"{num1} {num2}\n")

print(f"转换完成，结果保存在 {output_file}")
