import time
from .savedata import bubble_path_colddown, bubble_path_cdback
from .savedata import read_it, write_into

# 这里读起来太痛苦了，我都不知道为什么我没有写注释。不建议任何人阅读！！
def cold_down_xiadan(theid):
    response_log = read_it(bubble_path_colddown)
    lasttime = response_log.get(theid, False)
    thistime = time.time()
    if lasttime == False:
        response_log[theid] = thistime
        return True
    else:
        if (thistime - lasttime) >= 1800:
            response_log[theid] = thistime
            return True
        else:
            return False

def cold_down_back(theid):
    response_logback = read_it(bubble_path_cdback)
    lasttime = response_logback.get(theid, False)
    thistime = time.time()
    if lasttime == False:
        response_logback[theid] = thistime
        
        return True
    else:
        if (thistime - lasttime) >= 1800:
            response_logback[theid] = thistime
            return True
        else:
            return False
        
def cold_down_xiadan_write(theid):
    response_log = read_it(bubble_path_colddown)
    thistime = time.time()
    response_log[theid] = thistime
    write_into(bubble_path_colddown, response_log)

def cold_down_back_write(theid):
    response_logback = read_it(bubble_path_cdback)
    thistime = time.time()
    response_logback[theid] = thistime
    write_into(bubble_path_cdback, response_logback)