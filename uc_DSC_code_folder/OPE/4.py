import time
from get_circules import generate_tangent_circles_info, Point
from vet_vec_v_circule import get_vec_v
from Crypto.PublicKey import ECC
from myclass import Requester
from get_center import SquarePartition
from Crypto.Hash import SHA256
from Crypto.Random import random
import matplotlib.pyplot as plt


def hash_values(*values):
    """
    对传入的多个值进行哈希计算，返回哈希值的十六进制表示。
    """
    hash_obj = SHA256.new()
    for value in values:
        hash_obj.update(str(value).encode('utf-8'))
    return hash_obj.hexdigest()


def measure_execution_time(requester1, iterations, file_path):
    start_time = time.time()

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

        requester1.Location_Policy_Generation(level)

    end_time = time.time()
    execution_time_s = end_time - start_time  # 执行时间（秒）
    return execution_time_s


if __name__ == "__main__":
    # 定义曲线名称和迭代次数
    curves = ['P-192', 'P-224', 'P-256', 'P-384', 'P-521']
    iterations_list = [0, 500, 1000, 1500, 2000, 2500, 3000]
    level = 12  # 固定隐私保护等级

    # 创建一个字典来存储结果
    results = {curve: [] for curve in curves}

    file_path = "../dataset_process/same_block.txt"  # 数据文件路径

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

            exec_time = measure_execution_time(requester1, iterations, file_path)
            results[curve].append(exec_time)

    # 绘制结果
    plt.figure(figsize=(12, 8))

    # 定义不同的标记样式
    markers = ['o', 's', '^', 'D', 'x']

    for i, curve in enumerate(curves):
        plt.plot(iterations_list, results[curve], marker=markers[i % len(markers)], label=curve)

    plt.xlabel('Time Of Experiments')
    plt.ylabel('Computation Cost/s')
    plt.ylim(0, 45)  # 设置 y 轴范围
    plt.legend(title='Curve')
    plt.grid(True)
    plt.savefig('4.pdf')  # 将图形保存为 PDF 文件
    plt.show()  # 显示图形
