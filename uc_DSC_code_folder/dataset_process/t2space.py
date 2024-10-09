#将制表符转化为空格
def replace_tabs_with_spaces(input_file, output_file):
    with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
        for line in fin:
            # 将制表符替换为空格，并写入输出文件
            modified_line = line.replace('\t', ' ')
            fout.write(modified_line)

if __name__ == '__main__':
    input_file = 'C:/Users/z/Desktop/CopyThirdAndFourthColumns.txt'  # 替换为实际的输入文件名
    output_file = 'C:/Users/z/Desktop/ModifiedFile.txt'  # 替换为实际的输出文件名

    replace_tabs_with_spaces(input_file, output_file)
    print(f"Tabs replaced with spaces in {input_file}. Result saved in {output_file}.")
