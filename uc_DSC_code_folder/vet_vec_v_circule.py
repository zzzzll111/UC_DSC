def get_vec_v(G, circule, order):
    # 提取圆的参数
    x_c1 = circule.center.x
    y_c1 = circule.center.y
    R_1 = circule.r

    v_1 = 1
    v_2 = x_c1
    v_3 = y_c1
    v_4 = (x_c1 * x_c1 + y_c1 * y_c1 - R_1 * R_1)


    # 判断并处理负数情况
    if v_1 < 0 :
        v_1 = (order - 1) * (-v_1)
    if v_2 < 0:
        v_2 = (order - 1) * (-v_2)
    if v_3 < 0:
        v_3 = (order - 1) * (-v_3)
    if v_4 < 0:
        v_4 = (order - 1) * (-v_4)


    # 计算所需的点乘法
    v_1 = v_1 * G
    v_2 = v_2 * G
    v_3 = v_3 * G
    v_4 = v_4 * G


    return v_1, v_2, v_3, v_4
