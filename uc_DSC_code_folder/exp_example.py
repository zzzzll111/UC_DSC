from get_circules import generate_tangent_circles_info, Point
from vet_vec_v_circule import get_vec_v
from Crypto.PublicKey import ECC
from myclass import Worker, Requester, AES_ECB
from Crypto.Hash import SHA256


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
            ope_key_str,
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
    ope_key_str = '2354a78fbc6e5a1dab839c0f1aee6208'
    aes_ope = AES_ECB(ope_key_str)
    worker_location = Point(407249103345,-739946207517)
    ciphx = aes_ope.encode(str(worker_location.x))
    ciphy = aes_ope.encode(str(worker_location.y))
    H_x = SHA256.new(ciphx.encode('utf-8'))
    H_y = SHA256.new(ciphy.encode('utf-8'))
    H_ciphx = H_x.hexdigest()
    H_ciphy = H_y.hexdigest()

    # 定义文件路径和操作密钥
    file_path = 'dataset_process/same_block.txt'
    ope_key_str = '2354a78fbc6e5a1dab839c0f1aee6208'
    # 创建 Worker 对象列表
    workers = create_workers_from_file(file_path, 1000, ope_key_str, G, order, level_requester)

    # 统计通过验证的 worker
    verified_workers_count = 0
    for worker in workers:
        worker.Location_Record_Generation(worker.wo_location)
        worker.Location_Information_Generation()

        is_verified = worker.Location_Policy_Verification(requester1.v1, requester1.v2)

        if is_verified:
            verified_workers_count += 1  # 验证通过的计数器递增

    # 输出验证通过的 worker 数量
    print(f"验证通过的 Worker 数量: {verified_workers_count}")





