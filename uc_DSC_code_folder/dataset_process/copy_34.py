def copy_third_and_fourth_columns(input_file, output_file):
    with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
        for line in fin:
            # 去除行末的换行符，并按制表符分割行数据
            parts = line.strip().split('\t')

            # 确保每行至少有四列数据
            if len(parts) >= 4:
                # 提取第三列和第四列数据
                third_column = parts[2]
                fourth_column = parts[3]
                fout.write(f"{third_column}\t{fourth_column}\n")

if __name__ == '__main__':
    input_file = 'Gowalla_totalCheckins.txt'
    output_file = 'CopyThirdAndFourthColumns.txt'

    copy_third_and_fourth_columns(input_file, output_file)
    print(f"Third and fourth columns copied from {input_file} to {output_file}.")
