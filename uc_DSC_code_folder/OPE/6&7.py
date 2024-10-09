import json
from get_circules import generate_tangent_circles_info, Point
from vet_vec_v_circule import get_vec_v
from Crypto.PublicKey import ECC
from myclass import Requester
from get_center import SquarePartition
from Crypto.Hash import SHA256
from Crypto.Random import random
import matplotlib.pyplot as plt


def calculate_bit_length(value):
    """
    计算一个整数值的比特长度。
    """
    return value.bit_length()


def json_bit_length(data):
    """
    计算给定数据序列化为 JSON 后的比特长度。
    """
    json_str = json.dumps(data)
    return len(json_str) * 8  # 每个字符8比特


def hash_values(*values):
    """
    对传入的多个值进行哈希计算，返回哈希值的十六进制表示。
    """
    hash_obj = SHA256.new()
    for value in values:
        hash_obj.update(str(value).encode('utf-8'))
    return hash_obj.hexdigest()


def measure_json_bit_lengths(requester1, iterations, file_path):
    bit_lengths = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i in range(iterations):
        # 从文件中读取一行
        if i >= len(lines):
            break

        line = lines[i].strip()
        x_str, y_str = line.split()
        x = int(x_str)
        y = int(y_str)

        # 更新 requester1 的位置
        requester1.re_location = Point(x, y)

        # 重新计算中心和切线圆
        re_center_point = requester1_center.get_point_center(requester1.re_location)
        c1, c2 = generate_tangent_circles_info(re_center_point)

        # 重新计算 v 向量
        v_11, v_12, v_13, v_14 = get_vec_v(random_int_requester * G, c1, order)
        v_21, v_22, v_23, v_24 = get_vec_v(random_int_requester * G, c2, order)

        # 对 v 向量和公钥点坐标进行哈希计算
        v1_hash = hash_values(v_11, v_12, v_13, v_14)
        v2_hash = hash_values(v_21, v_22, v_23, v_24)
        str_v1 = f"{v_11} {v_12} {v_13} {v_14}"
        str_v2 = f"{v_21} {v_22} {v_23} {v_24}"


        g_hash = hash_values(G.x, G.y)
        str_G = f"{G.x},{G.y}"
        # 计算 JSON 格式的比特长度
        data = {
            "v1": str_v1,
            "v2": str_v2,
            "G": str_G,
            "v1_hash": v1_hash,
            "v2_hash": v2_hash,
            "g_hash": g_hash
        }

        bit_length = json_bit_length(data)
        bit_lengths.append(bit_length)

    return bit_lengths


if __name__ == "__main__":
    # 定义曲线名称和迭代次数
    curves = ['P-192', 'P-224', 'P-256', 'P-384', 'P-521']
    iterations_list = [0, 500, 1000, 1500, 2000, 2500, 3000]
    level = 12  # 固定隐私保护等级

    # 创建一个字典来存储结果
    results = {curve: [] for curve in curves}

    file_path = '../dataset_process/same_block.txt'  # 数据文件路径

    for curve in curves:
        # 生成 ECC 密钥对
        key = ECC.generate(curve=curve)
        G = key.pointQ
        curve_obj = ECC._curves[curve]
        order = curve_obj.order

        # 初始化常量
        random_int_requester = random.randint(1, 100000000000)  # 随机数
        requester1_center = SquarePartition(level)

        for iterations in iterations_list:
            # 创建 requester1 实例，初始位置可以是任意值，之后会被更新
            requester1 = Requester(random_int_requester * G, order,
                                   (0, 0, 0, 0),
                                   (0, 0, 0, 0),
                                   'sssssssss',
                                   Point(0, 0))  # 初始位置为 (0,0)

            bit_lengths = measure_json_bit_lengths(requester1, iterations, file_path)
            results[curve].append(bit_lengths[-1] if bit_lengths else 0)  # 取最后一个值

    # 输出所有 curve 对应的数值
    for curve in results:
        print(f"Curve: {curve}")
        for idx, bit_length in enumerate(results[curve]):
            print(f"Iteration {iterations_list[idx]}: {bit_length} bits")
        print()  # 每个曲线输出后换行

    # 绘制结果
    plt.figure(figsize=(12, 8))

    # 定义不同的标记样式
    markers = ['o', 's', '^', 'D', 'x']

    for i, curve in enumerate(curves):
        plt.plot(iterations_list, results[curve], marker=markers[i % len(markers)], label=curve)

    plt.xlabel('Number of Experiments')
    plt.ylabel('JSON Bit Length')
    plt.ylim(6000, 9000)  # 根据实际需要调整 y 轴范围
    plt.xlim(500, 3000)  # 根据实际需要调整 y 轴范围
    plt.legend(title='Curve')
    plt.grid(True)
    plt.savefig('6.pdf')  # 将图形保存为 PDF 文件
    plt.show()  # 显示图形
