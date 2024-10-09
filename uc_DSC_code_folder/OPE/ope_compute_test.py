#!/usr/bin/python3
import sys
import random
import pandas as pd
import time
import os
from opec import OpeClient
from ciphers import DumbCipher, AES_ECB, AES_ECB_192, AES_ECB_256
from pope import Pope
from cheater import Cheater
from mope import Mope
from oracle import Oracle


def get_hex_and_byte_length(data):
    """获取数据的十六进制表示和字节长度"""
    if isinstance(data, str):
        data = data.encode()  # 将字符串转换为字节对象
    hex_representation = data.hex()
    byte_length = len(data)
    return hex_representation, byte_length

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].startswith('-'):
        print("Runs some random correctness checks")
        print("Usage:", sys.argv[0], "[size] [seed]")
        exit(1)

    N = int(sys.argv[1]) if len(sys.argv) >= 2 else 1000
    seed = int(sys.argv[2]) if len(sys.argv) >= 3 else random.randrange(100000)

    random.seed(seed)
    print("seed is", seed)

    # 初始化 DataFrame 用于存储时间测量结果
    encode_times = []
    insert_times = []
    range_search_times = []
    communication_costs = []

    for algo in (Pope,):
        print("Checking {}...".format(algo.__name__))

        wordsfn = 'ope_test_number.txt'
        with open(wordsfn, 'r') as words:
            # 只读取前5000行
            wordlist = [line.strip() for _, line in zip(range(40000), words)]

        #        random.shuffle(wordlist)            #把txt里的东西都读取进wordlist,并打乱
        key_str = '2354a78fbc6e5a1dab839c0f1aee6208' #16字节
      #  key_str = '00112233445566778899aabbccddeeff0011223344556677' #24字节
     #   key_str = '00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff'  # 32字节
        crypt = AES_ECB(key_str)

        # 生成 pairs 列表
        pairs = []
        for word in wordlist:
            start_time = time.perf_counter()
            ciphertext = crypt.encode(word)
#           ciphertext_hex = ciphertext.hex()  # 将密文转换为十六进制字符串,已经是十六进制了
            end_time = time.perf_counter()
            encode_times.append((end_time - start_time) * 1000)  # 转换为毫秒
            pairs.append((word, ciphertext))  # 存储密文的十六进制字符串形式



        cl = OpeClient(algo(Oracle(crypt, 5)), crypt)
        checker = {}
        for (k, v) in pairs:
            start_time = time.perf_counter()
            cl.insert(k, v)
            end_time = time.perf_counter()
            insert_times.append((end_time - start_time) * 1000)  # 转换为毫秒
            checker[k] = v
        print("cl.size",cl.size() )



        ranges = [("999","506438845363"), ]
        for start, end in ranges:
            checkset = sorted((k,checker[k]) for k in checker if start <= k < end)
            res = sorted(cl.range_search(start,end))
            assert res == checkset


        key1 = '408873475173'
        key2 = '408873475175'

        # 测量范围搜索时间（毫秒）
        for _ in range(1000):
            start_time = time.perf_counter()
            rangesearch = cl.range_search(key1, key2)
            end_time = time.perf_counter()
            range_search_times.append((end_time - start_time) * 1000)  # 转换为毫秒

            for key, value, encrypted_key, encrypted_value in rangesearch:
                # 获取四个变量的十六进制表示和字节长度
                key_hex, key_byte_length = get_hex_and_byte_length(key)
                value_hex, value_byte_length = get_hex_and_byte_length(value)
                encrypted_key_hex, encrypted_key_byte_length = get_hex_and_byte_length(encrypted_key)
                encrypted_value_hex, encrypted_value_byte_length = get_hex_and_byte_length(encrypted_value)

                # 存储到列表
                communication_costs.append({
                    'Key': key_hex,
                    'Key字节长度': key_byte_length,
                    'Value(aes)': value_hex,
                    'Value(aes)字节长度': value_byte_length,
                    'Encrypted Key': encrypted_key_hex,
                    'Encrypted Key字节长度': encrypted_key_byte_length,
                    'Encrypted Value': encrypted_value_hex,
                    'Encrypted Value字节长度': encrypted_value_byte_length
                })

        # 创建 DataFrame
        df_encode_times = pd.DataFrame(encode_times, columns=['编码时间（毫秒）'])
        df_insert_times = pd.DataFrame(insert_times, columns=['插入时间（毫秒）'])
        df_range_search_times = pd.DataFrame(range_search_times, columns=['范围搜索时间（毫秒）'])
        df_communication_costs = pd.DataFrame(communication_costs)

        # 计算总开销和平均开销
        total_encode_time = df_encode_times['编码时间（毫秒）'].sum()
        average_encode_time = df_encode_times['编码时间（毫秒）'].mean()

        total_insert_time = df_insert_times['插入时间（毫秒）'].sum()
        average_insert_time = df_insert_times['插入时间（毫秒）'].mean()

        total_range_search_time = df_range_search_times['范围搜索时间（毫秒）'].sum()
        average_range_search_time = df_range_search_times['范围搜索时间（毫秒）'].mean()

        # 创建总开销和平均开销 DataFrame
        df_total_encode_time = pd.DataFrame({
            '编码时间（毫秒）': ['总开销', '平均开销'],
            '值': [total_encode_time, average_encode_time]
        })

        df_total_insert_time = pd.DataFrame({
            '插入时间（毫秒）': ['总开销', '平均开销'],
            '值': [total_insert_time, average_insert_time]
        })

        df_total_range_search_time = pd.DataFrame({
            '范围搜索时间（毫秒）': ['总开销', '平均开销'],
            '值': [total_range_search_time, average_range_search_time]
        })

        # 将总开销和平均开销合并到原 DataFrame 的最后一行
        df_encode_times = pd.concat([df_encode_times, df_total_encode_time], ignore_index=True)
        df_insert_times = pd.concat([df_insert_times, df_total_insert_time], ignore_index=True)
        df_range_search_times = pd.concat([df_range_search_times, df_total_range_search_time], ignore_index=True)

        # 打印当前工作目录
        print("当前工作目录是:", os.getcwd())

        # 保存到指定的 Excel 文件名
        with pd.ExcelWriter('40000.xlsx') as writer:
            df_encode_times.to_excel(writer, sheet_name='编码时间', index=False)
            df_insert_times.to_excel(writer, sheet_name='插入时间', index=False)
            df_range_search_times.to_excel(writer, sheet_name='范围搜索时间', index=False)
            df_communication_costs.to_excel(writer, sheet_name='通信开销', index=False)

        # 调用 range_search 方法并迭代结果
#        for decrypted_key, decrypted_value in cl.range_search(key1, key2):
#            print(f"Decrypted Key: {decrypted_key}, Decrypted Value: {decrypted_value}")

#        for decrypted_key, decrypted_value, encrypted_key, encrypted_value in cl.range_search(key1, key2):
#            print(f"Decrypted Key: {decrypted_key}, Decrypted Value: {decrypted_value},Encrypted Key: {encrypted_key}, Encrypted Value: {encrypted_value}")

        # for key, value in cl.range_search_test(key1, key2):
        #  print(f"Key: {key},Decrypted Value: {crypt.decode(key)}, Value: {value} ")



        #        ciphertext_pairs = cl.range_search_ciphertext(key1, key2)
        # 打印加密后的键值对
#        for enkey, enval in ciphertext_pairs:
#            print(f"Encrypted Key: {enkey}, Encrypted Value: {enval}")
        # 查看 OpeClient 的密钥 key
#        print(cl._crypt.key)  # 假设 cl 是已经创建好的 OpeClient 实例

        print("All checks passed!")
        print()



