from get_circules import *
import hashlib
import time
from get_center import SquarePartition
import zk_aes
from vet_vec_v_circule import get_vec_v
from vet_vec_u_workers import get_vec_u
from Crypto.Random import random
import sys
import random
from OPE.opec import OpeClient
from OPE.ciphers import DumbCipher, AES_ECB
from OPE.pope import Pope
from OPE.oracle import Oracle

class Worker:
    def __init__(self, OPE_key_x,OPE_key_y, ciphxs, ciphys, H_ciphxs, H_ciphys, pk_ECC, order, privacy_level, global_coords, now_coords, zk_proof_file, wo_location):
        self.OPE_key_x = OPE_key_x  # 存储 OPE x密钥的字符串
        self.OPE_key_y = OPE_key_y
        self.crypt_x = AES_ECB(OPE_key_x)
        self.crypt_y = AES_ECB(OPE_key_y)
        self.client_x = OpeClient(Pope(Oracle(self.crypt_x, 5)), self.crypt_x)
        self.client_y = OpeClient(Pope(Oracle(self.crypt_y, 5)), self.crypt_y)
        self.ciphxs = []  # 初始化空列表，用于存储 ciphx
        self.ciphxs.append(ciphxs)
        self.ciphys = []  # 初始化空列表，用于存储 ciphy
        self.ciphys.append(ciphys)
        self.H_ciphxs = []  # 初始化空列表，用于存储 ciphx 的哈希值
        self.H_ciphxs.append(H_ciphxs)
        self.H_ciphys = []  # 初始化空列表，用于存储 ciphy 的哈希值
        self.H_ciphys.append(H_ciphys)
        self.pk_ECC = pk_ECC  # 椭圆曲线生成元公钥
        self.order = order  # 椭圆曲线的阶
        self.privacy_level = privacy_level  # privacy_level（整数）
        self.global_coords = global_coords  # 四个经纬度上下限（global）
        self.now_coords = []  # 四个经纬度上下限（now）
        self.zk_proof_file = zk_proof_file  # 零知识证明文件存储位置
        self.wo_location = wo_location # worker的位置


    def __str__(self):
        return (f"Worker Details:\n"
                f"OPE_key: {self.OPE_key_x}\n"
                f"ciphs: {self.ciphxs}\n"
                f"ciphs: {self.ciphys}\n"
                f"H_ciphs: {self.H_ciphxs}\n"
                f"H_ciphs: {self.H_ciphys}\n"
                f"pk: {self.pk_ECC}\n"
                f"order: {self.order}\n"
                f"wo_point: {self.wo_location}\n"
                f"privacy_level: {self.privacy_level}\n"
                f"all_coords: {self.global_coords}\n"
                f"now_coords: {self.now_coords}\n"
                f"zk_proof_file: {self.zk_proof_file}\n"
                )

    #位置数据记录
    def Location_Record_Generation(self, point):

        # 用OPE加密x和y坐标
        ciphx = self.crypt_x.encode(str(point.x))
        ciphy = self.crypt_y.encode(str(point.y))
        print("ciphx is",ciphx)
        print("ciphy is",ciphy)
        self.client_x.insert(str(point.x), ciphx)
        self.client_y.insert(str(point.y), ciphy)
        # 计算ciphx和ciphy的SHA-256哈希值
        H_ciphx = hashlib.sha256(ciphx.encode('utf-8')).hexdigest()
        H_ciphy = hashlib.sha256(ciphy.encode('utf-8')).hexdigest()
        # 将ciphx添加到ciphxs列表中
        self.ciphxs.append(ciphx)
        self.ciphys.append(ciphy)

        # 将哈希值添加到对应的列表中
        self.H_ciphxs.append(H_ciphx)
        self.H_ciphys.append(H_ciphy)

        # 生成时间戳
        timestamp = int(time.time())
        # 返回 ciphx 在 ciphxs 列表中的序列

        index = self.ciphxs.index(ciphx)

        return (index, ciphx, ciphy, H_ciphx, H_ciphy, timestamp)

    #algorithm 3
    def Location_Policy_Verification(self, v1, v2):
        (v11,v12,v13,v14) = v1
        (v21,v22,v23,v24) = v2

        wo_center = SquarePartition(self.privacy_level)
        centerpoint = wo_center.get_point_center(self.wo_location)

        (u1, u2, u3, u4) = get_vec_u(self.pk_ECC,centerpoint,self.order)
        result1 = u1 * v11 + u2 * v12 + u3 * v13 + u4 * v14
        result2 = u1 * v21 + u2 * v22 + u3 * v23 + u4 * v24
        if result1.x == 0 and result1.y == 0 and result2.x == 0 and result2.y == 0:
            return True
        else:
            return False

    def Location_Information_Generation(self):

        wo_center = SquarePartition(self.privacy_level)
        (x_min,x_max,y_min,y_max) = wo_center.get_location_information(self.wo_location)
        try:
            self.now_coords.append((x_min, x_max, y_min, y_max))
            return True
        except AttributeError:
            # 如果 self.now_coords 不是列表，添加操作会失败
            return False

    def Location_Proof_Generation(self):

        (x_min, x_max, y_min, y_max) = self.now_coords[-1]
        x_min_ope = self.crypt_x.encode(str(x_min))
        x_max_ope = self.crypt_x.encode(str(x_max))
        y_min_ope = self.crypt_y.encode(str(y_min))
        y_max_ope = self.crypt_y.encode(str(y_max))

        snark_x_key = [int(self.OPE_key_x[i:i + 2], 16) for i in range(0, len(self.OPE_key_x), 2)]
        snark_y_key = [int(self.OPE_key_y[i:i + 2], 16) for i in range(0, len(self.OPE_key_y), 2)]
        # 将 wo_location 的坐标转换为 16 字节长的字节数组（需要填充零或截断）
        wo_location_x_str = f'{self.wo_location.x:032x}'  # 转换为32个字符的16进制数
        wo_location_y_str = f'{self.wo_location.y:032x}'  # 转换为32个字符的16进制数
        snark_x_message = [int(wo_location_x_str[i:i + 2], 16) for i in range(0, len(wo_location_x_str), 2)]
        snark_y_message = [int(wo_location_y_str[i:i + 2], 16) for i in range(0, len(wo_location_y_str), 2)]
        zk_aes.proof_generate(snark_x_message, snark_x_key)
        zk_aes.proof_generate(snark_y_message, snark_y_key)

        return (self.ciphxs[-1],self.ciphys[-1], x_min_ope, x_max_ope,y_min_ope, y_max_ope)




class Requester:
    def __init__(self, pk_ECC, order, v1, v2, blockchain_public_keys, re_location):
        self.pk_ECC = pk_ECC  # 椭圆曲线生成元公钥
        self.order = order  # 椭圆曲线的阶
        self.v1 = v1  # 椭圆曲线点 v1，表示 k1 * G
        self.v2 = v2  # 椭圆曲线点 v2，表示 k2 * G
        self.blockchain_public_keys = blockchain_public_keys  # 区块链公钥列表
        self.re_location = re_location


    def __str__(self):
        blockchain_keys_str = "\n".join([f"Blockchain Public Key {i+1}: {key}" for i, key in enumerate(self.blockchain_public_keys)])
        return (f"Requester Details:\n"
                f"Public Key (pk_G): {self.pk_ECC}\n"
                f"Order: {self.order}\n"
                f"v1: {self.v1}\n"  # 打印椭圆曲线点 v1
                f"v2: {self.v2}\n"  # 打印椭圆曲线点 v2
                f"re_point: {self.re_location}\n"
                f"Blockchain Public Keys:\n{blockchain_keys_str}")

    def Location_Policy_Generation(self,level):
        random_int_requester = random.randint(1, 100000000000)  # re的随机数
        requester1_center = SquarePartition(level)
        # re的中心位置
        re_center_point = requester1_center.get_point_center(self.re_location)
        # 用re的中心位置生成2个圆
        c1, c2 = generate_tangent_circles_info(re_center_point)
        # 获取 v 向量
        v_11, v_12, v_13, v_14 = get_vec_v(random_int_requester * self.pk_ECC, c1, self.order)
        v_21, v_22, v_23, v_24 = get_vec_v(random_int_requester * self.pk_ECC, c2, self.order)
        # 赋值
        self.v1 = (v_11, v_12, v_13, v_14)
        self.v2 = (v_21, v_22, v_23, v_24)

    def Location_Proof_Verification(self, worker, x_ope, y_ope, x_min_ope, x_max_ope, y_min_ope, y_max_ope):
        # 获取worker提供的加密位置数据范围
        x_range_results = list(worker.client_x.range_search(x_min_ope, x_max_ope))
        y_range_results = list(worker.client_y.range_search(y_min_ope, y_max_ope))

        # 检查x_ope是否在x范围的结果中
        x_in_range = any(
            x_ope == decode_enkey or x_ope == decode_enval or x_ope == encode_enkey or x_ope == encode_envalue
            for decode_enkey, decode_enval, encode_enkey, encode_envalue in x_range_results
        )

        # 检查y_ope是否在y范围的结果中
        y_in_range = any(
            y_ope == decode_enkey or y_ope == decode_enval or y_ope == encode_enkey or y_ope == encode_envalue
            for decode_enkey, decode_enval, encode_enkey, encode_envalue in y_range_results
        )

        zk_aes.proof_verify()


        if x_in_range and y_in_range:
            return 1
        else:
            return 0






