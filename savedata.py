import json


bubble_path_init = "C:\\Funart\\Main\\src\\plugins\\Funart\\temp\\dict_data.json"
bubble_path_random = "C:\\Funart\\Main\\src\\plugins\\Funart\\temp\\codes.json"
bubble_path_savedata = "C:\\Funart\\Main\\src\\plugins\\Funart\\temp\\group_ids.json"
bubble_path_backdoor= "C:\\Funart\\Main\\src\\plugins\\Funart\\temp\\backup.json"
bubble_path_traceback = "C:\\Funart\\Main\\src\\plugins\\Funart\\temp\\traceback.json"
bubble_path_colddown = "C:\\Funart\\Main\\src\\plugins\\Funart\\temp\\last_response.json"
bubble_path_cdback = "C:\\Funart\\Main\\src\\plugins\\Funart\\temp\\cdback.json"



# 读取
def read_it(filepth):
    with open(filepth, 'r') as file:
        bsket = json.load(file)
        file.close()
    return bsket

# 写入
def write_into(filepth, bsket):
    with open(filepth, 'w') as file:
        json.dump(bsket, file)
        file.close()


# 检查用户输入的群号是否受Funart支持
def check_group(groupid):
    # 读取群号配置文件中的内容
    group_basket = read_it(bubble_path_savedata)
    support_event = group_basket.get(groupid, False)
    if support_event == "once":
        return True
    else:
        return False

# 向群号配置文件添加群（仅限SUPERUSER）
def add_group(idnum):
    # 读取群号配置文件中的内容
    group_basket = read_it(bubble_path_savedata)
    initif = group_basket.get(idnum, False)
    if initif == "once":
        search_rst = "该群已被添加！"
    else:
        group_basket[idnum] = "once"
        search_rst = "添加成功"
        write_into(bubble_path_savedata, group_basket)
    return search_rst
