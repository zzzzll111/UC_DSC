#筛选掉精度太低的点
def delete_rows_with_short_numbers(input_file, output_file):
    with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
        for line in fin:
            parts = line.strip().split()
            if len(parts) < 2:
                continue

            num1 = parts[0].replace('-', '').replace('.', '')  # 去除正负号和小数点
            num2 = parts[1].replace('-', '').replace('.', '')

            if len(num1) < 11 or len(num2) < 11:
                continue

            # 如果两个数字都长度大于等于11，则写入输出文件
            fout.write(line)


def pad_numbers_to_13(input_file, output_file):
    with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
        for line in fin:
            parts = line.strip().split()
            if len(parts) < 2:
                continue

            num1 = parts[0].replace('-', '').replace('.', '')  # 去除正负号和小数点
            num2 = parts[1].replace('-', '').replace('.', '')

            # 补齐数字到13位，末尾补0
            num1_padded = num1.ljust(13, '0')
            num2_padded = num2.ljust(13, '0')

            # 替换原行中的数字部分
            parts[0] = parts[0].replace(num1, num1_padded)
            parts[1] = parts[1].replace(num2, num2_padded)

            # 将处理后的行数据重新组合，并写入输出文件
            fout.write('\t'.join(parts) + '\n')


if __name__ == '__main__':
    input_file = 'pad_to_13.txt'
    output_file1 = 'delete_less11.txt'  # 删除长度小于11的行后的输出文件路径
    output_file2 = 'pad_to_13.txt'  # 数字补齐到13位后的输出文件路径

    # 第一步：删除长度小于11的行
    delete_rows_with_short_numbers(input_file, output_file1)
    print(f"Rows with numbers shorter than 11 digits deleted. Result saved in {output_file1}.")

    # 第二步：将数字补齐到13位
    pad_numbers_to_13(output_file1, output_file2)
    print(f"All numbers padded to 13 digits. Result saved in {output_file2}.")

