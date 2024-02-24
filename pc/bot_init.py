# 自动连接初始化，创建机器人对象，命令行调用
import contextlib
import threading
from tcp_user import tcp_user
from get_bot_ipv4 import get_ip ,scan_ip

id_ip_dic = {} #机器人ID对应IP


def thread_connect(i):
    global bot_dic, bot_list
    print('尝试建立连接',i,':',get_ip()[i])
    with contextlib.suppress(Exception):
        if get_ip()[i] not in bot_dic:
            bot_dic[get_ip()[i]] = [tcp_user(get_ip()[i],'yuk2'),'yuk2']
            bot_dic[get_ip()[i]][0].thread_listen()
            bot_dic[get_ip()[i]][0].send_pass()
            print(i,get_ip()[i],'建立成功')

# 扫描可用ip
def init():
    '''初始化'''
    global bot_dic, bot_list
    scan_ip()

    # 生成机器人对象
    bot_dic = {}
    threads = [
        threading.Thread(
            target=thread_connect,
            args={
                i,
            },
        )
        for i in range(len(get_ip()))
    ]
    for i in threads:
        i.start()

def liveip():
    global bot_dic
    print(get_ip()) # 查看当前建立的连接
    print('可用连接:',bot_dic)

def send():
    '''/send [8] 233'''
    global cmd_list, bot_dic, id_ip_dic
    ip = id_ip_dic[cmd_list[1]]
    print(ip)

    bot_dic[ip][0].send_data(cmd_list[2])

def binding_ip_id():
    global bot_dic, id_ip_dic
    for i in bot_dic:
        id_ip_dic[ bot_dic[i][0].bot_aruco_id ] = i

def cmd(cmds):
    '''
    拆分字符,定向发送
    - /liveip 查看当前已经建立的连接
    - /rescan 从新扫描并建立新的连接
    - /send [8] /wryyyyy 向 机器人[8] 发送 /wryyyyy
    - /line [8] x y 令 机器人[8] 沿直线运动到(x,y)
    - /arc [9] x0 y0 x1 y1 令 机器人[8] 以(x0,y0)为圆心 短弧为轨迹 运动到 (x1,y1)
    '''
    global bot_dic, cmd_list
    CMD_RUN = [rescan, liveip, send]
    binding_ip_id()

    cmd_list = cmds.split()

    if cmd_list[0][0] == '/':
        CMD_CLASS = ['/rescan', '/liveip', '/send']
        for i in range(len(CMD_CLASS)):
            if CMD_CLASS[i] == cmd_list[0]:
                try:
                    CMD_RUN[i]() # 调用指定命令
                except Exception:
                    print('不存在该指令 或 语法错误')

def remove_bot_dic(dic_ip):
    '''移除bot对象'''
    global bot_dic
    if dic_ip in bot_dic:
        bot_dic.pop(dic_ip)

def rescan():
    '''排除已连接ip从新扫描'''
    global bot_dic
    scan_ip()
    threads = [
        threading.Thread(
            target=thread_connect,
            args={
                i,
            },
        )
        for i in range(len(get_ip()))
    ]
    for i in threads:
        i.start()


