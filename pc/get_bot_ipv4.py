# -*- coding: utf-8 -*-

import platform
import os
import time
import threading
import socket
 
live_ip = 0
live_ip_list = []
 
 
def get_os():
    os = platform.system()
    if os == "Windows":
        return "n"
    else:
        return "c"
 
 
def ping_ip(ip_str):
    cmd = ["ping", "-{op}".format(op=get_os()),
           "1", ip_str]
    output = os.popen(" ".join(cmd)).readlines()
    for line in output:
        if str(line).upper().find("TTL") >= 0:
            print("ip: %s 在线" % ip_str)
            global live_ip, live_ip_list
            live_ip += 1
            live_ip_list.append(ip_str)
            break
 
 
def find_ip(ip_prefix):
    '''''
    给出当前的ip地址段 ，然后扫描整个段所有地址
    '''
    threads = []
    for i in range(1, 256):
        ip = '%s.%s' % (ip_prefix, i)
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
    ipv4s=socket.gethostbyname_ex(socket.gethostname())[2][0]
    return ipv4s

def scan_ip():
    global live_ip_list
    live_ip_list = []
    print("开始扫描时间: %s" % time.ctime())
    addr = find_local_ip()
    args = "".join(addr)
    ip_pre = '.'.join(args.split('.')[:-1])
    find_ip(ip_pre)
    print("扫描结束时间 %s" % time.ctime())
    print('本次扫描共检测到本网络存在%s台设备' % live_ip)
    
def get_ip():
    global live_ip_list
    return live_ip_list