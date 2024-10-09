import time
from get_circules import generate_tangent_circles_info, Point
from vet_vec_v_circule import get_vec_v
from Crypto.PublicKey import ECC
from myclass import Requester
from get_center import SquarePartition
from Crypto.Hash import SHA256
from Crypto.Random import random
import matplotlib.pyplot as plt
from myclass import *

def hash_values(*values):
    """
    对传入的多个值进行哈希计算，返回哈希值的十六进制表示。
    """
    hash_obj = SHA256.new()
    for value in values:
        hash_obj.update(str(value).encode('utf-8'))
    return hash_obj.hexdigest()


def measure_execution_time(requester1, iterations, file_path, worker1):
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

        # 更新 worker1 的位置
        worker1.wo_location = Point(x, y)

        worker1.Location_Policy_Verification(requester1.v1,requester1.v2)

    end_time = time.time()
    execution_time_s = end_time - start_time  # 执行时间（秒）
    return execution_time_s


if __name__ == "__main__":
    # 定义曲线为固定的 'P-192'，并设置隐私保护等级从 5 到 18
    curve = 'P-192'
    levels = list(range(5, 19))  # 隐私保护等级从 5 到 18
    iterations_list = [0, 500, 1000, 1500, 2000, 2500, 3000]

    # 创建一个字典来存储结果
    results = {level: [] for level in levels}

    file_path = "../dataset_process/same_block.txt"  # 数据文件路径

    # 生成 ECC 密钥对
    key = ECC.generate(curve=curve)
    G = key.pointQ
    curve_obj = ECC._curves[curve]
    order = curve_obj.order

    for level in levels:
        requester1_center = SquarePartition(level)

        for iterations in iterations_list:
            # 生成随机数
            random_int_requester = random.randint(1, 100000000000)  # 随机数

            # 创建 requester1 实例，初始位置可以是任意值，之后会被更新
            requester1 = Requester(random_int_requester * G, order,
                                   (0, 0, 0, 0),
                                   (0, 0, 0, 0),
                                   'sssssssss',
                                   Point(0, 0))  # 初始位置为 (0,0)
            # 设置worker初始参数,以便初始化
            ope_key_str_x = '2354a78fbc6e5a1dab839c0f1aee6208'
            ope_key_str_y = '2354a78fbc6e5a1dab839c0f1aee6208'
            aes_ope_x = AES_ECB(ope_key_str_x)
            aes_ope_y = AES_ECB(ope_key_str_x)
            worker_location = Point(407249103345, -739946207517)
            ciphx = aes_ope_x.encode(str(worker_location.x))
            ciphy = aes_ope_y.encode(str(worker_location.y))
            H_x = SHA256.new(ciphx.encode('utf-8'))
            H_y = SHA256.new(ciphy.encode('utf-8'))
            H_ciphx = H_x.hexdigest()
            H_ciphy = H_y.hexdigest()
            worker1 = Worker(ope_key_str_x, ope_key_str_y, ciphx, ciphy, H_ciphx, H_ciphy, G, order, level,
                             'global_coords', [], 'zk_proof_file', worker_location)
            requester1.re_location = Point(407249103345, -739946207517)
            requester1.Location_Policy_Generation(level)
            exec_time = measure_execution_time(requester1, iterations, file_path, worker1)
            results[level].append(exec_time)

    # 绘制结果
    plt.figure(figsize=(12, 8))

    # 定义不同的标记样式
    markers = ['o', 's', '^', 'D', 'x', 'v', '<', '>', 'p', '*']

    for i, level in enumerate(levels):
        plt.plot(iterations_list, results[level], marker=markers[i % len(markers)], label=f'Level {level}')

    plt.xlabel('Privacy Level n')
    plt.ylabel('Computation Cost/s')
    plt.ylim(0, 10)  # 设置 y 轴范围
    plt.legend(title='Privacy Protection Level')
    plt.grid(True)
    plt.savefig('5.pdf')  # 将图形保存为 PDF 文件
    plt.show()  # 显示图形
