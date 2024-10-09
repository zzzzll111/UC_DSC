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
from openpyxl import Workbook
import json

if __name__ == "__main__":
    # 定义曲线为固定的 'P-192'
    curve = 'P-192'
    level = 12
    iterations_list = [0, 5, 10, 15, 20, 25, 30]  # 试验次数
    file_path = "../dataset_process/same_block.txt"  # 数据文件路径

    # 生成 ECC 密钥对
    key = ECC.generate(curve=curve)
    G = key.pointQ
    curve_obj = ECC._curves[curve]
    order = curve_obj.order
    re_location = Point(407413881970, -739894545078)  # re的实际位置
    c1, c2 = generate_tangent_circles_info(re_location)  # re的实际位置所在的中心点以及两个相切的圆
    v_11, v_12, v_13, v_14 = get_vec_v(G, c1, order)  # 此时的v是明文，为了方便实例化requester1
    v_21, v_22, v_23, v_24 = get_vec_v(G, c2, order)
    requester1 = Requester(G, order,  # 实例化一个requester1
                           (v_11, v_12, v_13, v_14),
                           (v_21, v_22, v_23, v_24),
                           'sssssssss',
                           re_location)

    requester1.Location_Policy_Generation(level)

    # 设置worker初始参数，以便初始化
    ope_key_str_x = '2354a78fbc6e5a1dab839c0f1aee6208'
    ope_key_str_y = '2354a78fbc6e5a1dab839c0f1aee6208'
    aes_ope_x = AES_ECB(ope_key_str_x)
    aes_ope_y = AES_ECB(ope_key_str_y)
    worker_location = Point(407249103345, -739946207517)
    ciphx = aes_ope_x.encode(str(worker_location.x))
    ciphy = aes_ope_y.encode(str(worker_location.y))
    H_x = SHA256.new(ciphx.encode('utf-8'))
    H_y = SHA256.new(ciphy.encode('utf-8'))
    H_ciphx = H_x.hexdigest()
    H_ciphy = H_y.hexdigest()
    worker1 = Worker(ope_key_str_x, ope_key_str_y, ciphx, ciphy, H_ciphx, H_ciphy, G, order, level,
                     'global_coords', [], 'zk_proof_file', worker_location)

    # 读取文件内容
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 创建一个新的Excel工作簿和工作表
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Execution Time"
    sheet.append(["Iterations", "Total Execution Time (seconds)"])

    for iterations in iterations_list:
        total_time = 0.0
        for i in range(iterations):
            if i >= len(lines):
                break
            line = lines[i].strip()
            x_str, y_str = line.split()  # 从文件中读取 x 和 y 的值
            x = int(x_str)
            y = int(y_str)

            # 更新 worker1 的位置
            (index, ciphx, ciphy, H_ciphx, H_ciphy, timestamp) = worker1.Location_Record_Generation(Point(x, y))
            worker1.Location_Information_Generation()

            (ciphxs, ciphys, x_min_ope, x_max_ope, y_min_ope, y_max_ope) = worker1.Location_Proof_Generation()

            data = {
                "ciphxs": ciphxs,
                "ciphys": ciphys,
                "x_min_ope": x_min_ope,
                "x_max_ope": x_max_ope,
                "y_min_ope": y_min_ope,
                "y_max_ope": y_max_ope
            }

            # 将字典转换为 JSON 格式字符串
            json_str = json.dumps(data)

            # 计算 JSON 字符串的比特数
            bit_count = len(json_str.encode('utf-8')) * 8

            # 输出结果
            print(f"JSON 格式的比特数: {bit_count} bits")

            print(f"Location Proof Size {bit_count+6840+6072} bits")
