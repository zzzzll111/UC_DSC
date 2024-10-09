def main():
    # 输入文件和输出文件路径
    input_file = r'pad_to_13.txt'
    output_file = r'beijing.txt'

    # 打开输入文件和输出文件
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        # 逐行读取输入文件
        for line in f_in:
            # 去除行首尾空白符并按空格分割得到纬度和经度
            latitude, longitude = line.strip().split()

            # 将纬度和经度转换为浮点数
            latitude = float(latitude)
            longitude = float(longitude)

            # 判断经纬度是否在指定范围内
            if (39.45 <= latitude <= 40.05) and (116.20 <= longitude <= 116.30):
                # 写入满足条件的经纬度到输出文件
                f_out.write(f"{latitude} {longitude}\n")


if __name__ == "__main__":
    main()
