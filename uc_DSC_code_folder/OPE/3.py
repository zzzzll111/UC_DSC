from get_circules import generate_tangent_circles_info, Point
from vet_vec_v_circule import get_vec_v
from Crypto.PublicKey import ECC
from myclass import Worker, Requester, AES_ECB
from Crypto.Hash import SHA256
import sys
import random
from opec import OpeClient
from ciphers import DumbCipher, AES_ECB
from pope import Pope
from oracle import Oracle
import random
import time
import matplotlib.pyplot as plt


def create_workers_from_file(file_path, num_workers, ope_key_str, G, order, level_requester):
    workers = []

    # 创建 AES_ECB 实例

    aes_ope = AES_ECB(ope_key_str)

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if i >= num_workers:
            break

        # 读取每行数据，分割并转换为整数
        x_str, y_str = line.strip().split()
        x = int(x_str)
        y = int(y_str)

        # 创建 worker_location 点对象
        worker_location = Point(x, y)

        # 计算加密值和哈希值
        ciphx = aes_ope.encode(str(worker_location.x))
        ciphy = aes_ope.encode(str(worker_location.y))
        H_x = SHA256.new(ciphx.encode('utf-8'))
        H_y = SHA256.new(ciphy.encode('utf-8'))
        H_ciphx = H_x.hexdigest()
        H_ciphy = H_y.hexdigest()

        # 实例化 Worker 对象
        test_worker = Worker(
            ope_key_str_x,
            ope_key_str_y,
            ciphx,
            ciphy,
            H_ciphx,
            H_ciphy,
            G,  # 需要根据上下文定义
            order,  # 需要根据上下文定义
            level_requester,  # 隐私保护等级
            'global_coords',  # 可以根据实际情况修改
            [],  # 初始为空列表
            'zk_proof_file',  # 零知识证明文件
            worker_location
        )

        workers.append(test_worker)

    return workers

def print_worker_details(workers, num_to_print=10):
    for i, worker in enumerate(workers[:num_to_print]):
        print(f"Worker {i + 1}:")
        print(f"  Location (x, y): ({worker.wo_location.x}, {worker.wo_location.y})")
        print(f"  Encrypted X: {worker.ciphxs[-1]}")
        print(f"  Encrypted Y: {worker.ciphys[-1]}")
        print(f"  Hash of Encrypted X: {worker.H_ciphxs[-1]}")
        print(f"  Hash of Encrypted Y: {worker.H_ciphys[-1]}")
        print(f"  Public Key ECC: {worker.pk_ECC}")
        print(f"  Order: {worker.order}")
        print(f"  Privacy Level: {worker.privacy_level}")
        print(f"  Global Coordinates File: {worker.global_coords}")
        print(f"  Current Coordinates: {worker.now_coords}")
        print(f"  Zero-Knowledge Proof File: {worker.zk_proof_file}")
        print()

if __name__ == "__main__":
    # 生成椭圆曲线密钥对，可选的有：192，224，256，384，521，
    key = ECC.generate(curve='P-192')
    # 获取公钥的点对象
    G = key.pointQ
    # 获取椭圆曲线的标识字符串
    curve_name = key.curve
    # 根据标识字符串获取椭圆曲线对象
    curve = ECC._curves[curve_name]
    # 获取椭圆曲线的阶
    order = curve.order
    level_requester = 12  # 隐私保护等级
    #根据level等级，获取点所在的区域中心
    re_location = Point(407413881970, -739894545078) #re的实际位置
    c1, c2 = generate_tangent_circles_info(re_location) #re的实际位置所在的中心点.以及两个相切的圆
    v_11, v_12, v_13, v_14 = get_vec_v(G, c1, order)#此时的v是明文，为了方便实例化requester1
    v_21, v_22, v_23, v_24 = get_vec_v(G, c2, order)
    requester1 = Requester(G, order, #实例化一个requester1
                           (v_11, v_12, v_13, v_14),
                           (v_21, v_22, v_23, v_24),
                           'sssssssss',
                           re_location)


    requester1.Location_Policy_Generation(level_requester)


   #设置worker初始参数,以便初始化
    ope_key_str_x = '2354a78fbc6e5a1dab839c0f1aee6208'
    ope_key_str_y = '2354a78fbc6e5a1dab839c0f1aee6208'
    aes_ope_x = AES_ECB(ope_key_str_x)
    aes_ope_y = AES_ECB(ope_key_str_x)
    worker_location = Point(407249103345,-739946207517)
    ciphx = aes_ope_x.encode(str(worker_location.x))
    ciphy = aes_ope_y.encode(str(worker_location.y))
    H_x = SHA256.new(ciphx.encode('utf-8'))
    H_y = SHA256.new(ciphy.encode('utf-8'))
    H_ciphx = H_x.hexdigest()
    H_ciphy = H_y.hexdigest()

    # 定义文件路径和操作密钥
    file_path = '../dataset_process/same_block.txt'

    # 创建 Worker 对象
    worker1 = Worker(ope_key_str_x,ope_key_str_y,ciphx,ciphy,H_ciphx,H_ciphy,G,order, level_requester, 'global_coords', [], 'zk_proof_file', worker_location)

    worker_location = Point(407249103355, -739946207557)
    worker1.Location_Record_Generation(worker_location)

    worker_location = Point(507249103355, -839946207557)
    worker1.Location_Record_Generation(worker_location)

    worker_location = Point(607249103355, -939946207557)
    worker1.Location_Record_Generation(worker_location)

    # 初始化时间和测试次数
    execution_times = []
    test_iterations = [0, 500, 1000, 1500, 2000, 2500, 3000]

    # 执行多次操作并记录时间
    for n in test_iterations:
        start_time = time.time()
        worker_location = Point(407249103355, -739946207557)
        for i in range(n):
            if i >= 2:
                worker_location.x += random.randint(0, 100)
                worker_location.y -= random.randint(0, 100)
            worker1.Location_Record_Generation(worker_location)
        end_time = time.time()
        execution_times.append((end_time - start_time) * 1000)  # 转为毫秒

    # 绘制时间开销曲线
    plt.figure()
    plt.plot(test_iterations, execution_times, marker='o')
    plt.xlabel('Time Of Experiments')
    plt.ylabel('Computation Cost/ms')
    plt.grid(True)

    # 在每个点处标注纵坐标的数值
    for i, txt in enumerate(execution_times):
        plt.annotate(f'{txt:.2f}', (test_iterations[i], execution_times[i]), textcoords="offset points", xytext=(0, 10),
                     ha='center')

    # 保存并展示图表
    plt.savefig("3.pdf")
    plt.show()


