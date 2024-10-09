import os
import glob
import shutil
import re

# 从块文件重构原始文件的函数
def bin_file_reconstruct(folder_path, output_folder):
    try:
        # 如果输出文件夹不存在，则创建它
        os.makedirs(output_folder, exist_ok=True)

        # 获取文件夹中的所有块文件
        block_files = glob.glob(os.path.join(folder_path, "*"))

        if len(block_files) == 0:
            # 如果没有块文件，则不执行任何操作
            print(f"文件夹中未找到块文件: {folder_path}")
        elif len(block_files) == 1:
            # 如果只有一个块文件，修改其名称并复制到输出文件夹
            original_file_name = os.path.basename(block_files[0])
            new_file_name = re.sub(r'_[0-9]+', '', original_file_name)  # 移除下划线和数字部分
            output_file_path = os.path.join(output_folder, os.path.splitext(new_file_name)[0])  # 移除扩展名
            shutil.copyfile(block_files[0], output_file_path)
            print(f"单个文件复制并保存在: {output_file_path}")
        else:
            # 根据文件名中的数值部分对块文件进行排序
            block_files.sort(key=lambda x: extract_number_from_filename(x))

            # 读取每个块的内容并重构原始文件内容
            file_content = b''
            for block_file in block_files:
                with open(block_file, 'rb') as f:
                    file_content += f.read()

            # 根据文件夹名称确定输出文件路径和名称
            output_file_path = os.path.join(output_folder, os.path.basename(folder_path))

            # 将重构的内容写入输出文件
            with open(output_file_path, 'wb') as output_file:
                output_file.write(file_content)

            print(f"文件重构并保存在: {output_file_path}")
    except Exception as e:
        print(f"重构过程中发生错误: {str(e)}")

# 从文件名中提取数值部分的函数
def extract_number_from_filename(filename):
    match = re.search(r'\d+', os.path.basename(filename))
    return int(match.group()) if match else float('inf')

