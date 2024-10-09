from Crypto.PublicKey import ECC


def get_vec_u(G, worker_center, order):
    # 提取圆的参数


    u_1 = worker_center.x * worker_center.x + worker_center.y * worker_center.y
    u_2 = -2 * worker_center.x
    u_3 = -2 * worker_center.y
    u_4 = 1


    # 判断并处理负数情况
    if u_1 < 0 :
        u_1 = (order - 1) * (-u_1)
    if u_2 < 0:
        u_2 = (order - 1) * (-u_2)
    if u_3 < 0:
        u_3 = (order - 1) * (-u_3)
    if u_4 < 0:
        u_4 = (order - 1) * (-u_4)


    return u_1, u_2, u_3, u_4
