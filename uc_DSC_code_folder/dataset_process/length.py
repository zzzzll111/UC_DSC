#求长度
def count_digit_lengths(input_file):
    # 初始化长度为0到13的计数器为0
    count_col1 = {i: 0 for i in range(14)}
    count_col2 = {i: 0 for i in range(14)}

    with open(input_file, 'r') as fin:
        for line in fin:
            # 去除行末的换行符，并按空格分割行数据
            parts = line.strip().split()

            if len(parts) < 2:
                continue

            # 第1列数字的长度统计
            num1 = parts[0].replace('-', '').replace('.', '')  # 去除正负号和小数点
            num1_length = sum(c.isdigit() for c in num1)  # 统计数字字符的个数

            if num1_length <= 13:
                count_col1[num1_length] += 1

            # 第2列数字的长度统计
            num2 = parts[1].replace('-', '').replace('.', '')  # 去除正负号和小数点
            num2_length = sum(c.isdigit() for c in num2)  # 统计数字字符的个数

            if num2_length <= 13:
                count_col2[num2_length] += 1

    return count_col1, count_col2


if __name__ == '__main__':
    input_file = 'pad_to_13.txt'

    count_col1, count_col2 = count_digit_lengths(input_file)
    print("Column 1 digit length counts (excluding signs and decimals):")
    for length, count in count_col1.items():
        print(f"Length {length}: {count} occurrences")

    print("\nColumn 2 digit length counts (excluding signs and decimals):")
    for length, count in count_col2.items():
        print(f"Length {length}: {count} occurrences")

