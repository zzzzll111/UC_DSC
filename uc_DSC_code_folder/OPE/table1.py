import time
from get_circules import generate_tangent_circles_info, Point
from vet_vec_v_circule import get_vec_v
from Crypto.PublicKey import ECC
from myclass import Requester
from get_center import SquarePartition
from Crypto.Hash import SHA256
from Crypto.Random import random
from openpyxl import Workbook
from myclass import AES_ECB, Worker
import json
if __name__ == "__main__":
    # 定义曲线为固定的 'P-192'
    curve = 'P-521'
    level = 12
    iterations = 30  # 固定运行30次
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

    # 设置worker初始参数, 以便初始化
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

    (index, ciphx, ciphy, H_ciphx, H_ciphy, timestamp) = worker1.Location_Record_Generation(worker_location)

    # 将生成的数据转换为 JSON 格式
    data_dict = {
        "index": index,
        "ciphx": ciphx,
        "ciphy": ciphy,
        "H_ciphx": H_ciphx,
        "H_ciphy": H_ciphy,
        "timestamp": timestamp
    }

    # 转换为 JSON 字符串
    json_data = json.dumps(data_dict)

    # 计算 JSON 字符串的比特数
    bit_count = len(json_data.encode('utf-8')) * 8

    print(f"Location_Record_Generation的JSON 数据的总比特数: {bit_count} bits")

    requester1.Location_Policy_Generation(level)
    (v_11,v_12,v_13,v_14) = requester1.v1
    (v_21,v_22,v_23,v_24) = requester1.v2
    publickey = G
# 强制转换为字符串
data_dict = {
    "v_11": str(v_11),
    "v_12": str(v_12),
    "v_13": str(v_13),
    "v_14": str(v_14),
    "v_21": str(v_21),
    "v_22": str(v_22),
    "v_23": str(v_23),
    "v_24": str(v_24),
    "publickey": str(publickey)
}

# 将字典转换为 JSON 字符串
json_data = json.dumps(data_dict)

# 计算 JSON 字符串的比特数
bit_count = len(json_data.encode('utf-8')) * 8

print(f"Location Policy JSON 数据的总比特数: {bit_count} bits")
worker1.Location_Information_Generation()
(ciphxs,ciphys, x_min_ope, x_max_ope,y_min_ope, y_max_ope) = worker1.Location_Proof_Generation()
# 强制转换为字符串并封装为字典
data_dict = {
    "ciphx_last": str(ciphxs),
    "ciphy_last": str(ciphys),
    "x_min_ope": str(x_min_ope),
    "x_max_ope": str(x_max_ope),
    "y_min_ope": str(y_min_ope),
    "y_max_ope": str(y_max_ope)
}

# 将字典转换为 JSON 字符串
json_data = json.dumps(data_dict)

# 计算 JSON 字符串的比特数
bit_count = len(json_data.encode('utf-8')) * 8

print(f"JSON 数据的总比特数: {bit_count} bits")