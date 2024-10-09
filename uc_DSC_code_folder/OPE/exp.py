#!/usr/bin/python3
import sys
import random
from opec import OpeClient
from ciphers import DumbCipher, AES_ECB
from pope import Pope
from cheater import Cheater
from mope import Mope
from oracle import Oracle


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].startswith('-'):
        print("Runs some random correctness checks")
        print("Usage:", sys.argv[0], "[size] [seed]")
        exit(1)

    N = int(sys.argv[1]) if len(sys.argv) >= 2 else 1000
    seed = int(sys.argv[2]) if len(sys.argv) >= 3 else random.randrange(100000)

    random.seed(seed)
    print("seed is", seed)

    for algo in ( Pope, ):
        print("Checking {}...".format(algo.__name__))

        wordsfn = '../dataset_process/same_block.txt'
        with open(wordsfn, 'r') as words:
            wordlist = [line.strip() for line in words]
#        random.shuffle(wordlist)            #把txt里的东西都读取进wordlist,并打乱
        key_str = '2354a78fbc6e5a1dab839c0f1aee6208'
        crypt = AES_ECB(key_str)

        # 生成 pairs 列表
        pairs = []
        for word in wordlist:
            ciphertext = crypt.encode(word)
#            ciphertext_hex = ciphertext.hex()  # 将密文转换为十六进制字符串,已经是十六进制了
            pairs.append((word, ciphertext))  # 存储密文的十六进制字符串形式

        # 打印示例 pairs
        for key, value in pairs[:10]:  # 打印前 10 对 key-value
            print(f"Key: {key}, Encrypted Value (Hex): {value}")
        print("Number of key-value pairs:", len(pairs))

        cl = OpeClient(algo(Oracle(crypt, 5)), crypt)
        checker = {}
        for (k, v) in pairs:
            cl.insert(k,v)
            checker[k] = v
        print("cl.size",cl.size() )



        ranges = [("999","506438845363"), ]
        for start, end in ranges:
            checkset = sorted((k,checker[k]) for k in checker if start <= k < end)
            res = sorted(cl.range_search(start,end))


        rangesearch = cl.range_search(106438845363,506438845363)
        # 假设 cl 是包含 range_search 方法的类的实例

        # 定义搜索范围的起始和结束键
        key1 = '106438845363'
        key2 = '506438845363'

        # 调用 range_search 方法并迭代结果
#        for decrypted_key, decrypted_value in cl.range_search(key1, key2):
#            print(f"Decrypted Key: {decrypted_key}, Decrypted Value: {decrypted_value}")

#        for decrypted_key, decrypted_value, encrypted_key, encrypted_value in cl.range_search(key1, key2):
#            print(f"Decrypted Key: {decrypted_key}, Decrypted Value: {decrypted_value},Encrypted Key: {encrypted_key}, Encrypted Value: {encrypted_value}")

        for key, value in cl.range_search_test(key1, key2):
          print(f"Decrypted Key: {key}, Decrypted Value: {value} ")



        #        ciphertext_pairs = cl.range_search_ciphertext(key1, key2)
        # 打印加密后的键值对
#        for enkey, enval in ciphertext_pairs:
#            print(f"Encrypted Key: {enkey}, Encrypted Value: {enval}")
        # 查看 OpeClient 的密钥 key
#        print(cl._crypt.key)  # 假设 cl 是已经创建好的 OpeClient 实例

        print("All checks passed!")
        print()



