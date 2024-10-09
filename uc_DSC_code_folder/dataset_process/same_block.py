input_file = r'conver2int.txt'
output_file = r'same_block.txt'

# 定义正方形区块的边界范围
blocks = {
    'block1': {'x_range': (-1800000000000, -900000000000), 'y_range': (-900000000000, 0)},
    'block2': {'x_range': (-900000000000, 0), 'y_range': (-900000000000, 0)},
    'block3': {'x_range': (0, 900000000000), 'y_range': (-900000000000, 0)},
    'block4': {'x_range': (900000000000, 1800000000000), 'y_range': (-900000000000, 0)},
    'block5': {'x_range': (-1800000000000, -900000000000), 'y_range': (0, 900000000000)},
    'block6': {'x_range': (-900000000000, 0), 'y_range': (0, 900000000000)},
    'block7': {'x_range': (0, 900000000000), 'y_range': (0, 900000000000)},
    'block8': {'x_range': (900000000000, 1800000000000), 'y_range': (0, 900000000000)}
}

# 给定的点
given_point = (300000000000, -600000000000)  # 例如：这里假设给定点是 (300000000000, -600000000000)

# 找到给定点所属的区块
block_name = None
for name, block_info in blocks.items():
    x_min, x_max = block_info['x_range']
    y_min, y_max = block_info['y_range']
    x_given, y_given = given_point

    if x_min <= x_given <= x_max and y_min <= y_given <= y_max:
        block_name = name
        break

if block_name is None:
    print("给定点不在任何区块范围内。")
else:
    print(f"给定点 ({given_point[0]}, {given_point[1]}) 属于区块 {block_name}。")

    # 打开输入文件和输出文件
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # 分割每行的数字对
            tokens = line.strip().split()
            if len(tokens) != 2:
                continue

            # 将每个数字转换为整数
            x = int(tokens[0])
            y = int(tokens[1])

            # 判断点属于同一区块
            if block_name in blocks:
                x_min, x_max = blocks[block_name]['x_range']
                y_min, y_max = blocks[block_name]['y_range']

                if x_min <= x <= x_max and y_min <= y <= y_max:
                    # 写入符合条件的点到输出文件
                    outfile.write(f"{x} {y}\n")

    print(f"属于同一区块的点已保存在 {output_file}")
