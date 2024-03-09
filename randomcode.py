import random
import string

from .savedata import bubble_path_random, read_it, write_into

punct = '!#$%&()*+,-.:;<=>?@[]^_{|}~'

# 构建验证码字符集合
characters = string.ascii_letters + string.digits + punct


# 这个是生成随机验证码的函数
# 2024.2.18 是不是有问题？会出现生成的字符连带着后面的文字内容被吞掉的情况，是生成了转义字符吗？
def generate_verification_code():
    while True:
        # 生成随机验证码
        code = ''.join(random.choice(characters) for _ in range(9))
        # 读取已生成过的验证码
        generated_codes = read_it(bubble_path_random)
        # 判断随机验证码是否重复
        repeated = generated_codes.get(code, False)
        if repeated == False:
            pass
        else:
            continue
        # 添加生成的全新验证码进入json文件
        # 为了保证键值对应，以code作为键，固定以"once"作为值
        # 比起我个人不擅长的数据库，可能还是直接作为集合写入文件更稳定
        generated_codes[code] = "once"
        #写入文件
        write_into(bubble_path_random, generated_codes)
        return code


# 检查验证码是否存在
def verify_codes(trycode):
    generated_codes = read_it(bubble_path_random)
    init_key = generated_codes.get(trycode, False)
    if init_key == "once":
        return True
    if init_key == False:
        return False
    else:
        return "Unexpected Error"