import filecmp
import os

def compare_files(file1, file2):
    try:
        if not os.path.isfile(file1):
            return f"文件不存在: {file1}"
        if not os.path.isfile(file2):
            return f"文件不存在: {file2}"

        # 使用 filecmp 模块比较文件内容
        if filecmp.cmp(file1, file2, shallow=False):
            return "相同"
        else:
            return "不同"
    except Exception as e:
        return f"比对文件时发生错误: {str(e)}"

