# 自动连接初始化，创建机器人对象，命令行调用
import contextlib
import threading
from tcp_user import tcp_user
from get_bot_ipv4 import get_ip ,scan_ip
import move_control as control

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

def set_cmdlist(list_):
    global cmd_list
    cmd_list = list_

def liveip():
    global bot_dic
    print(get_ip()) # 查看当前建立的连接
    print('可用连接:',bot_dic)

def send():
    '''
    cmd_list : /send [8] 233
    '''
    global cmd_list, bot_dic, id_ip_dic
    ip = id_ip_dic[cmd_list[1]]
    date = ''
    for _ in range(2, len(cmd_list)):
        date += cmd_list[_]
        date += ' '
    with contextlib.suppress(Exception):
        bot_dic[ip][0].send_data(date)

def binding_ip_id():
    '''使机器人id与ip一一对应'''
    global bot_dic, id_ip_dic
    for i in bot_dic:
        id_ip_dic[ bot_dic[i][0].bot_aruco_id ] = i

def line():
    '''
    cmd_list : /line [8] x y e r
    '''
    global cmd_list, bot_dic, id_ip_dic
    
    goal_x = float(cmd_list[2])
    goal_y = float(cmd_list[3])

    line_task = threading.Thread(target=control.line_move, args=(goal_x, goal_y, cmd_list[1], cmd_list[4], cmd_list[5], 1))
    line_task.start()
    print('线程line指令已经对>>>', cmd_list[1], '<<<开始执行，期间不可对其执行其他指令')

def arc():
    '''
    cmd_list : /arc [8] r, cita, rp, e
    '''
    global cmd_list, bot_dic, id_ip_dic
    
    line_task = threading.Thread(target=control.arc_move, args=(float(cmd_list[2]), int(cmd_list[3]), cmd_list[1], int(cmd_list[4]), int(cmd_list[5])))
    line_task.start()
    print('线程arc指令已经对>>>', cmd_list[1], '<<<开始执行，期间不可对其执行其他指令')


def rot():
    '''
    cmd_list : /rot [8] a c
    '''
    global cmd_list, bot_dic, id_ip_dic
    line_task = threading.Thread(target=control.rot_move, args=(cmd_list[1], cmd_list[2], cmd_list[3]))
    line_task.start()
    print('线程rot指令已经对', cmd_list[1], '开始执行，期间不可对其执行其他指令')

def rotp():
    '''
    cmd_list : /rotp [8] x y c
    '''
    global cmd_list, bot_dic, id_ip_dic
    line_task = threading.Thread(target=control.rotp_move, args=(cmd_list[1], float(cmd_list[2]), float(cmd_list[3]), float(cmd_list[4])))
    line_task.start()
    print('线程rotp指令已经对', cmd_list[1], '开始执行，期间不可对其执行其他指令')

def help():
    print('''
    - /liveip 【查看当前已经建立的连接】
    - /rescan 【从新扫描并建立新的连接】
    - /send [8] /show 【向 机器人[8] 发送 /show】
    - /line [8] x y a r 【令 机器人[8] 沿直线运动到(x,y) 角度容许误差为a 目标半径为r】
    - /arc [9] x0 y0 x1 y1 【令 机器人[8] 以(x0,y0)为圆心 短弧为轨迹 运动到 (x1,y1)】
    - /rot [8] a c 【令 机器人[8] 旋转到角度a 容许角度误差为c】
    - /rotp [8] x y c 【令 机器人[8] 旋转并指向(x,y) 容许角度误差为c】
    - /arc [8] r, cita, rp, e 【令 机器人[8] 以半径r旋转cita角度】
    ''')

def cmd(cmds):
    '''
    拆分字符, 执行函数
    '''
    global bot_dic, cmd_list
    CMD_RUN = [rescan, liveip, send, line, rot, rotp, arc, help]
    binding_ip_id()

    cmd_list = cmds.split()

    if cmd_list[0][0] == '/':
        CMD_CLASS = ['/rescan', '/liveip', '/send', '/line', '/rot', '/rotp', '/arc', '/help']
        for i in range(len(CMD_CLASS)):
            if CMD_CLASS[i] == cmd_list[0]:
                try:
                    CMD_RUN[i]() # 调用指定命令
                except Exception:
                    print('不存在该指令 或 语法错误')
                    print('输入/help查看指令')

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


