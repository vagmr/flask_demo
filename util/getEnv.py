"""
@文件        :getEnv.py
@说明        :从.env文件中读取环境变量
@时间        :2024/01/16 14:06:59
@作者        :vagmr
@版本        :1.1
"""


import os
import sys

# 获取当前项目的根目录
root_path = sys.path[1]
env_path = os.path.join(root_path, '.env')
env_dict = {}


def dict_init():
    """
    从.env文件中提取键值对，初始化一个字典。该函数会检查.env文件
    是否存在，逐行读取内容，从值中移除空格和引号，并跳过注释
    和空行。如果没有找到.env文件，将抛出异常。

    异常：
        如果在给定的路径下未找到`.env`文件，抛出异常。
    """
    if os.path.exists(env_path):
        print("找到.env文件")
    else:
        raise Exception("未找到.env文件")
    with open(env_path, 'r', encoding='utf-8') as env_file:
        for line in env_file:
            # print(line)
            # 去除空格和换行符
            line = line.strip()
            # 跳过注释行和空行
            if not line or line.startswith('#'):
                continue
            # 将行分割成键和值
            if '=' in line:
                key, value = line.split('=', 1)
                # 去除值两边的空格和引号
                value = value.strip().strip('\'"')
                env_dict[key] = value


def init_env():
    """
    如果env_dict为空，则调用dict_init函数来加载环境变量。
    """
    if not env_dict:  # 如果 env_dict 是空的，则加载环境变量
        dict_init()


def get_env(key):
    """
    根据提供的键(key)，从环境变量字典(env_dict)中获取值。
    如果键不存在，则抛出异常。

    参数:
        key (str): 要检索的环境变量的键。

    返回:
        str: 对应于键的环境变量的值。

    异常:
        Exception: 如果键在环境变量字典中不存在。
    """
    if key in env_dict:
        return env_dict[key]
    else:
        raise Exception("未找到%s环境变量" % key)


if __name__ == '__main__':
    dict_init()
    print(env_dict)
