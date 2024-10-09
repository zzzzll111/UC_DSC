import os
import math

# 计算文件大小（以比特为单位）
def file_size_in_bits(file_path):
    try:
        # 获取文件的字节大小
        size_bytes = os.path.getsize(file_path)
        # 将字节转换为比特
        size_bits = size_bytes * 8
        return size_bits
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except Exception as e:
        print(f"计算文件大小时发生错误: {str(e)}")

# 将文件分割成256比特的块，并保存到指定文件夹
def split_file_into_blocks(file_path, output_folder):
    try:
        # 如果输出文件夹不存在，则创建它
        os.makedirs(output_folder, exist_ok=True)

        # 以二进制模式打开输入文件
        with open(file_path, 'rb') as f:
            # 读取整个文件内容
            file_content = f.read()
            # 计算需要的块数
            block_size_bits = 256
            num_blocks = math.ceil(len(file_content) * 8 / block_size_bits)

            # 在输出文件夹中写入每个块到单独的文件中
            for i in range(num_blocks):
                block_start = i * block_size_bits // 8
                block_end = min((i + 1) * block_size_bits // 8, len(file_content))
                block_data = file_content[block_start:block_end]

                # 格式化块编号，以三位数带前导零的形式
                block_number = f"{i + 1:03}"  # 例如，001, 002, ..., 999

                # 构造块文件路径（不含扩展名）
                block_file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}_{block_number}.bin"
                block_file_path = os.path.join(output_folder, block_file_name)

                # 将块数据写入文件
                with open(block_file_path, 'wb') as block_file:
                    block_file.write(block_data)

            print(f"文件 {file_path} 成功分割为 {num_blocks} 个块.")
    except Exception as e:
        print(f"分割文件时发生错误: {str(e)}")

# 主函数，将多个文件分割为块并保存到指定文件夹中
def bin_file_split(file_paths, output_folder):
    # 遍历每个文件路径
    for path in file_paths:
        # 将文件分割为块并保存到输出文件夹中
        split_file_into_blocks(path, output_folder)