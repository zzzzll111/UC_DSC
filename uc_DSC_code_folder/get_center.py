# 假设从 get_circules 模块中导入 Point 类
from get_circules import Point

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


class SquarePartition:
    def __init__(self, level):
        self.level = level
        self.side_length = int(900000000000 / (2 ** (level)))  # 计算每个级别下正方形的边长
        self.block_count = 2 ** (level + 1)  # 计算每个级别下正方形的数量（每边划分为 2^(level-1) 个正方形）

    def get_block(self, point):
        x = point.x
        y = point.y
        for block_name, block_info in blocks.items():
            x_range = block_info['x_range']
            y_range = block_info['y_range']
            if x_range[0] <= x < x_range[1] and y_range[0] <= y < y_range[1]:
                return block_name, x_range, y_range
        return None, None, None

    def get_point_center(self, point):
        block_name, x_range, y_range = self.get_block(point)
        if block_name:
            # 计算在该 block 内 x 和 y 的整数倍 side_length
            center_x = int(point.x - (point.x - x_range[0]) % self.side_length + self.side_length / 2)
            center_y = int(point.y - (point.y - y_range[0]) % self.side_length + self.side_length / 2)
            center = Point(center_x, center_y)
            return center
        else:
            return None

    def get_location_information(self, point):
        block_name, x_range, y_range = self.get_block(point)
        if block_name:
            # 计算在该 block 内 x 和 y 的整数倍 side_length
            center_x = int(point.x - (point.x - x_range[0]) % self.side_length + self.side_length / 2)
            center_y = int(point.y - (point.y - y_range[0]) % self.side_length + self.side_length / 2)
            center_x_min = int(center_x - self.side_length / 2)
            center_x_max = int(center_x + self.side_length / 2)
            center_y_min = int(center_y - self.side_length / 2)
            center_y_max = int(center_y + self.side_length / 2)

            return center_x_min, center_x_max, center_y_min, center_y_max
        else:
            return None


# 示例用法
if __name__ == "__main__":
    level = 22  # 最高11级
    partition = SquarePartition(level)


    given_point = Point(-1000000000000, 500000000000)

    # 获取该点所属的 block 以及该 block 的范围
    block_name, x_range, y_range = partition.get_block(given_point)
    print(f"Point ({given_point.x}, {given_point.y}) belongs to {block_name}")
    print(f"Block Range: x_range={x_range}, y_range={y_range}")
    # 获取该点所在的正方形中心
    center = Point(0,0)
    center = partition.get_point_center(given_point)
    print({center.x, center.y})
    print(given_point.x, given_point.y)
    assert((center.x, center.y) == (given_point.x, given_point.y))



