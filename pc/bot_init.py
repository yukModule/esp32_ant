# 自动连接初始化，创建机器人对象，命令行调用

from tcp_user import tcp_user
from get_bot_ipv4 import get_ip ,scan_ip

# 扫描可用ip
def init():
    '''初始化'''
    global bot_dic, ip_num, bot_list
    scan_ip()
    ip_num = len(get_ip())

    # 生成机器人对象
    bot_list = [_ for _ in range(ip_num)] 
    bot_dic = {}

    # 筛选可用连接
    for i in range(ip_num):
        print('尝试建立连接',i,':',get_ip()[i])
        try:
            if get_ip()[i] in bot_dic:
                pass
            else:
                bot_list[i] = tcp_user(get_ip()[i],'yuk2')
                bot_list[i].thread_listen()
                bot_list[i].send_pass()
                print(i,get_ip()[i],'建立成功')
                bot_dic[get_ip()[i]] = [bot_list[i],'yuk2']
        except:
            print(i,get_ip()[i],'不可用或没有开启TCP服务器')

    print('可用连接:',bot_dic)

def cmd(cmds):
    '''
    拆分字符,定向发送
    - /liveip 查看当前已经建立的连接
    - /rescan 从新扫描并建立新的连接
    - 192.168.xxx.xxx:/wryyyyy 向192.168.xxx.xxx发送wryyyyy
    '''
    global bot_dic
    if cmds[0] == '/':
        if cmds == '/liveip':
            print(get_ip()) # 查看当前建立的连接
            print('可用连接:',bot_dic)
        if cmds == '/rescan':
            rescan() # 排除已经建立的 从新建立连接

    else:
        try:
            list_1 = cmds.split(':')
            bot_dic[list_1[0]][0].send_data(list_1[1])
        except:
            print('语法错误 或 ip不存在')

def remove_bot_dic(dic_ip):
    '''移除bot对象 '''
    global bot_dic
    if dic_ip in bot_dic:
        bot_dic.pop(dic_ip)

def rescan():
    '''排除已连接ip从新扫描'''
    global bot_dic, bot_list
    scan_ip()
    for i in range(ip_num):
        print('尝试建立连接',i,':',get_ip()[i])
        try:
            if get_ip()[i] in bot_dic:
                pass
            else:
                bot_list[i] = tcp_user(get_ip()[i],'yuk2')
                bot_list[i].thread_listen()
                bot_list[i].send_pass()
                print(i,get_ip()[i],'建立成功')
                bot_dic[get_ip()[i]] = [bot_list[i],'yuk2']
        except:
            print(i,get_ip()[i],'不可用或没有开启TCP服务器')
    print('可用连接:',bot_dic)