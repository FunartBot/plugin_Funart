from .colddown import cold_down_xiadan, cold_down_back
from .colddown import cold_down_xiadan_write, cold_down_back_write
from .randomcode import generate_verification_code, verify_codes
from .savedata import read_it, write_into, check_group, add_group
from .savedata import bubble_path_init, bubble_path_backdoor, bubble_path_traceback

from nonebot import on_command
from nonebot.adapters import Message, Event
from nonebot.params import ArgPlainText, CommandArg
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.typing import T_State

from nonebot.adapters.onebot.v11 import Bot, Message


sendback = on_command("联系FA", rule=to_me(), aliases={"联系Fa", "联系fa", "联系fA"}, block=True, priority=70)
helpsign = on_command("帮助", rule=to_me(), block=True, priority=60)
sign = on_command("下单", rule=to_me(), priority=50)
traceback = on_command("反向留号", rule=to_me(), block=True, priority=55)
fareply = on_command("代回", rule=to_me(), block=True, priority=40)
# 规划了群内代回复功能，但出于“会不会在群里拉扯导致刷屏？”的考量，一直没着手实现
query = on_command("查询", rule=to_me(), block=True, priority=51)
addgroup = on_command("添加支持", rule=to_me(), permission=SUPERUSER, block=True, priority=5)


@sendback.handle()
async def _(event: Event, bot: Bot, args: Message = CommandArg()):
    sender_id = event.get_user_id()
    if sendtext := args.extract_plain_text():
        # 转发一条消息至测试群
        leave_msg = "来自用户【" + sender_id + "】的留言：" + "\n" + sendtext
        await bot.send_group_msg(group_id=933095247, message=leave_msg, auto_escape=True)
        await sendback.finish("您的留言已经转发至开发者测试群，感谢反馈！")
    else:
        await sendback.finish("请在指令后附上反馈信息！\
                              \n格式为：/联系FA 你要说的话")


@helpsign.handle()
async def handle_help():
    await helpsign.finish("下单前，请务必阅读Funart用户手册：\
                          \nhttps://docs.qq.com/doc/DTUNGZEh3RExyTm9Q")


@sign.got("groupid", prompt="【请发送您需Funart代下单的群聊群号】\n若需退出进程，可发送“quit”；\n注意：本进程若被长时间放置将会自动关闭，请尽量将bot每条消息的等待时间控制在2分钟内，建议提前准备好文案再触发指令！\n若本进程自动关闭，您可重新触发“/下单”命令。")
async def _(event: Event, state: T_State, groupid: str = ArgPlainText()):
    signsender = event.get_user_id()
    if cold_down_xiadan(signsender):
        pass
    else:
        await sign.finish("检测到您在30分钟内已经使用Funart下过单，请稍等哦！")
    state["signsender"] = signsender
    if groupid == "quit":
        # 若用户输入quit，则结束进程
        await sign.finish("下单进程结束")
    else:
        # 检测群号是否受支持
        state["groupid"] = groupid
        support_bool = check_group(groupid)
        if support_bool == True:
            pass
        else:
            # 群号不受支持，要求重新输入或退出
            await sign.reject(f"FunartBot暂不支持您输入的群聊,或您的输入非法。\
                              \n（您的输入为：{groupid}）\
                              \n请重新输入，或发送‘quit’结束输入！\
                              \n您也可以向acupofsheep@126.com发送邮件提供群聊支持建议，或使用“/联系FA”指令向开发者留言。")

@sign.got("logup", prompt="【请发送您的下单文案（暂时不支持图片）】\n注意：可通过输入“quit”结束进程。")
async def _(state: T_State, logup: str = ArgPlainText()):
    notraw_logup = logup.strip()
    if bool(notraw_logup):
        if logup == "quit":
            await sign.finish("下单进程结束！")
        else:
            state["logup"] = logup
    else:
        await sign.reject("下单文案不可为空，请重新输入！")

@sign.got("yourinfo", prompt="【请发送您的留号信息】\n若不想留号，可发送“pass”，对方将无法通过查询获得您的信息，只能通过Funart向您传递留号信息")
async def _(state: T_State, yourinfo: str = ArgPlainText()):
    notraw_yourinfo = yourinfo.strip()
    if bool(notraw_yourinfo):
        if yourinfo == "pass":
            # 覆盖yourinfo
            yourinfo = "对方没有留号，但您仍可通过Funart向对方发送您的留号信息。请使用“/反向留号”指令，根据引导操作"
        # 存取数据，准备进入下一个事件处理器
        logup = state["logup"]
        state["yourinfo"] = yourinfo
        # 发送最后一次确认消息
        devtext = "请再次确认您的下单文案内容和留号信息！" + "\n【文案内容】\n" + logup + "\n【留号信息】\n" + yourinfo + "\n若无误，请发送‘yes’正式下单；若有误，发送‘no’退出进程，重新开始。"
        await sign.send(devtext)
    else:
        await sign.reject("留号信息不可为空，请重新输入！")

@sign.got("yesor")
async def _(bot: Bot, state: T_State, yesor: str = ArgPlainText()):
    if yesor == "yes":
        # 生成验证码
        vcode = generate_verification_code()
        # 读取前一个事件处理器中的数据
        logup = state["logup"]
        groupid = state["groupid"]
        yourinfo = state["yourinfo"]
        # 读取留号信息文件
        data_with_codes = read_it(bubble_path_init)
        # 以验证码为键值，向字典data_with_codes中存储留号信息
        data_with_codes[vcode] = yourinfo
        # 将字典数据写入文件
        write_into(bubble_path_init, data_with_codes)
        final_text = vcode + "\n" + logup
        # 为防止恶意利用Funart发送不良信息，留一个用于追溯信息源的记录
        signsender = state["signsender"]
        sender_dict = read_it(bubble_path_backdoor)
        sender_dict[vcode] = signsender
        write_into(bubble_path_backdoor, sender_dict)
        # 发送消息
        await bot.send_group_msg(group_id=int(groupid), message=final_text, auto_escape=True)
        cold_down_xiadan_write(signsender)
        await sign.finish(f"已尝试发送，验证码为【{vcode}】。若群内没有出现您的消息，请尝试向开发者反馈")
    if yesor == "no":
        await sign.finish("已为您退出进程，请重新开始")
    else:
        await sign.reject("输入非法，请在‘yes’或‘no’中选择，并重新输入")


@traceback.got("trycodee", prompt="请发送您需要通过Funart联系的验证码：")
async def _(event: Event, state: T_State, trycodee: str = ArgPlainText()):
    backsender = event.get_user_id()
    if cold_down_back(backsender):
        pass
    else:
        await traceback.finish("检测到您在30分钟内已经使用Funart反向留号过，请稍等哦！")
    state["trycodee"] = trycodee
    backdoor_dict = read_it(bubble_path_backdoor)
    once_id = backdoor_dict.get(trycodee, False)
    if once_id == False:
        await traceback.finish("查询不到此验证码，请检查是否输入错误，如确认无误，请向开发者反馈。\n注意：验证码为9位随机字符，不包括换行符，请优先检查是否有漏字、末尾换行！")
    else:
        state["once_id"] = once_id

@traceback.got("backinfo", prompt="请发送您的反向留号信息（不可为空）：")
async def _(bot: Bot, event: Event, state: T_State, backinfo: str = ArgPlainText()):
    once_id = state["once_id"]
    trycodee = state["trycodee"]
    notraw_backinfo = backinfo.strip()
    if bool(notraw_backinfo):
        sendback_id = event.get_user_id()
        fix_code_id = trycodee + sendback_id
        traceback_dict = read_it(bubble_path_traceback)
        traceback_dict[backinfo] = fix_code_id
        write_into(bubble_path_traceback, traceback_dict)
        sendback_dev = "戏友留言：通过验证码【" + trycodee + "】，留言内容为：\n" + backinfo
        cold_down_back_write(sendback_id)
        await bot.send_msg(message_type="private", user_id=int(once_id), message=sendback_dev)
        await traceback.finish("已尝试发送您的留言，请耐心等待！")
    else:
        await traceback.reject("反向留号信息不可为空！")


#@fareply.got("请发送您需Funart代回复的群聊**群号**\n若需退出进程，可发送“quit”\n注意：本进程若被长时间放置将会自动关闭，请尽量将bot每条消息的等待时间控制在2分钟内，建议提前准备好文案再触发指令！")
#async def _(bot: Bot, event: Event, state: T_State, groupid: str = ArgPlainText()):
    #sender = event.get_user_id()


@query.got("trycode", prompt="请发送您需要查询的验证码")
async def _(trycode: str = ArgPlainText()):
    initsult = verify_codes(trycode)
    if initsult == True:
        data_with_codes = read_it(bubble_path_init)
        backinfo = data_with_codes[trycode]
        await query.finish(f"对方留下的信息为：{backinfo}")
    else:
        await query.finish("查询不到此验证码，请检查是否输入错误，如确认无误，请向开发者反馈！")


@addgroup.got("idnum", prompt="请输入要添加的群号")
async def _(idnum: str = ArgPlainText()):
    searchre = add_group(idnum)
    await addgroup.finish(searchre)
