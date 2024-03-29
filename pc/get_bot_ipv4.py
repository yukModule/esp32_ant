# 获取连接本机热点的ipv4地址

import platform
import os
import time
import threading
import socket

ipv4_pc = ''
live_ip = 0
live_ip_list = []


def get_os():
    os = platform.system()
    return "n" if os == "Windows" else "c"


def ping_ip(ip_str):
    cmd = ["ping", "-{op}".format(op=get_os()),
           "1", ip_str]
    output = os.popen(" ".join(cmd)).readlines()
    for line in output:
        if "TTL" in str(line).upper():
            print(f"ip: {ip_str} 在线")
            global live_ip, live_ip_list
            live_ip += 1
            live_ip_list.append(ip_str)
            break


def find_ip(ip_prefix):
    '''''
    给出当前的ip地址段 ，然后扫描整个段所有地址
    '''
    global ipv4_pc
    threads = []
    for i in range(1, 256):
        ip = f'{ip_prefix}.{i}'
        if ip!=ipv4_pc and ip not in live_ip_list:
            threads.append(threading.Thread(target=ping_ip, args={ip, }))
    for i in threads:
        i.start()
    for i in threads:
        i.join()

def find_local_ip():
    """
    获取本机当前ipv4地址
    :return: 返回本机ipv4地址
    """
    global ipv4_pc
    ipv4_pc=socket.gethostbyname_ex(socket.gethostname())[2][0]
    return ipv4_pc


def scan_ip():
    global live_ip_list
    print(f"开始扫描时间: {time.ctime()}")
    addr = find_local_ip()
    args = "".join(addr)
    print('本机ip:', args)
    ip_pre = '.'.join(args.split('.')[:-1])
    find_ip(ip_pre)
    print(f"扫描结束时间 {time.ctime()}")
    print(f'本次扫描共检测到本网络存在{live_ip}台设备')


def get_ip():
    '''返回扫描已连接的ipv4'''
    global live_ip_list
    return live_ip_list


def remove_ip(list_):
    '''清除已不可用的ip'''
    global live_ip_list
    if list_ in live_ip_list:
        live_ip_list.remove(list_)