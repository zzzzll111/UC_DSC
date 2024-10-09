#对每个level，查看符合要求的点一共是多少


from get_circules import generate_tangent_circles_info, Point
from vet_vec_v_circule import get_vec_v
from Crypto.PublicKey import ECC
from vet_vec_u_workers import get_vec_u
from get_center import SquarePartition
from myclass import Requester
from tqdm import tqdm

if __name__ == "__main__":
    # 生成椭圆曲线密钥对
    key = ECC.generate(curve='P-256')
    # 获取公钥的点对象
    G = key.pointQ
    # 获取椭圆曲线的标识字符串
    curve_name = key.curve
    # 根据标识字符串获取椭圆曲线对象
    curve = ECC._curves[curve_name]
    # 获取椭圆曲线的阶
    order = curve.order
    # 需要运行的不同隐私保护等级范围
    levels = range(10, 21)

    for level_requester in levels:
        print(f"当前处理隐私保护等级: {level_requester}")

        # 根据level等级，获取点所在的区域中心
        requester1_center = SquarePartition(level_requester)

        re_location = Point(407809180092, -739810265391)  # re的实际位置
        c1, c2 = generate_tangent_circles_info(re_location)  # 为了实例化requester1
        v_11, v_12, v_13, v_14 = get_vec_v(G, c1, order)
        v_21, v_22, v_23, v_24 = get_vec_v(G, c2, order)

        requester1 = Requester(G, order,
                               (v_11, v_12, v_13, v_14),
                               (v_21, v_22, v_23, v_24),
                               'sssssssss',
                               re_location)

        # re的中心位置
        re_center_point = requester1_center.get_point_center(requester1.re_location)
        # 用re的中心位置生成2个圆
        c1, c2 = generate_tangent_circles_info(re_center_point)
        # 获取 v 向量
        v_11, v_12, v_13, v_14 = get_vec_v(G, c1, order)
        v_21, v_22, v_23, v_24 = get_vec_v(G, c2, order)
        # 赋值
        requester1.v1 = (v_11, v_12, v_13, v_14)
        requester1.v2 = (v_21, v_22, v_23, v_24)

        # 定义结果计数器
        count = 0

        # 打开文件并逐行读取，添加进度条
        file_path = fr"C:\Users\z\Desktop\{level_requester}.txt"
        with open(file_path, 'w') as result_file:
            # 打开待处理的文件
            input_file_path = r"C:\Users\z\Desktop\same_block.txt"
            with open(input_file_path, 'r') as file:
                # 获取文件行数
                num_lines = sum(1 for line in file)
                file.seek(0)  # 重新回到文件开头

                # 使用 tqdm 添加进度条
                for line_number, line in tqdm(enumerate(file, start=1), total=num_lines, desc=f"Processing level {level_requester} lines"):
                    tokens = line.strip().split()
                    if len(tokens) != 2:
                        continue

                    # 将数字转换为整数并创建 Point 对象
                    try:
                        x = int(tokens[0])
                        y = int(tokens[1])
                        point = Point(x, y)
                    except ValueError:
                        continue

                    # 获取点的中心位置
                    wi_center = requester1_center.get_point_center(point)
                    # 获取 v 向量
                    u_1, u_2, u_3, u_4 = get_vec_u(G, wi_center, order)

                    # 计算结果
                    result1 = u_1 * v_11 + u_2 * v_12 + u_3 * v_13 + u_4 * v_14
                    result2 = u_1 * v_21 + u_2 * v_22 + u_3 * v_23 + u_4 * v_24

                    # 检查是否符合要求
                    if result1.x == 0 and result1.y == 0 and result2.x == 0 and result2.y == 0:
                        count += 1
                        result_file.write(f"符合要求的点：行数={line_number}, x={point.x}, y={point.y}, 中心：x={wi_center.x},{wi_center.y}, 当前找到={count}\n")

        print(f"检查通过！共找到 {count} 个符合要求的点，并已保存到文件：{file_path}")
