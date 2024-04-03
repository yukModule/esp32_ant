import network
import socket
import time
import control
import WS2812
from save_load import *
import _thread
from time import sleep

WS2812.setColor(255, 0, 0)
SSID = get_config_var()['SSID']  # WiFi名称
PASSWORD = get_config_var()['PASSWORD']  # WiFi密码
port = 7788  # 端口号
wlan = None  # wlan
listenSocket = None  # 套接字
ret, conn = None, None
first_send = 1
CMD_CLASS = ['/connect', '/say2wifi', '/say2inf', '/m', '/sleep', '/setcolor', '/name', '/show', '/team', '/randomcolor']

class cmd:
    '''命令行接口'''
    
    def __init__(self):
        self.cmd_list = []
        self.CMD_RUN = [self.connect, self.say2wifi, self.say2inf, self.move, self.sleep, self.setcolor, self.name, self.show, self.team, self.randomcolor]
        self.sleep_or_wake = 'wake'
        self.ws2812_color = ['0', '0', '0']
        self.bot_name = 'Ant'
        self.bot_team = 'A'

    def split_(self,s):
        '''拆分字符串'''
        self.cmd_list = s.split()

    def allocation_cmd(self):
        '''判断并分类指令'''
        if self.cmd_list[0][0] != '/':
            return False
        for i in range(len(CMD_CLASS)):
            if CMD_CLASS[i] == self.cmd_list[0]:
                try:
                    self.CMD_RUN[i]() # 调用指定命令
                except Exception:
                    send2wifi('cmd error')
                return True
    
    def input_(self,s):
        self.split_(s)
        return self.allocation_cmd()
    
    def connect(self):
        '''/connect <wifi名> <wifi密码> # 设置wifi名与密码 并 链接 开启TCP服务器'''
        ssid =  self.cmd_list[1]
        password = self.cmd_list[2]
        set_password(ssid, password)
        creat_server()
        config_dict['SSID'] = self.cmd_list[1]
        config_dict['PASSWORD'] = self.cmd_list[2]
        save_()

    def say2wifi(self):
        '''/say2wifi <信息> # 通过wifi发送信息'''
        send2wifi(self.cmd_list[1])
    
    def say2inf(self):
        '''/say2inf <信息> # 通过红外发送信息''' 
        print(self.cmd_list[1])
    
    def move(self):
        '''/m <左电机pwm> <右电机pwm> # 控制电机转速'''
        if self.sleep_or_wake == 'wake':
            control.set_motor(self.cmd_list[1], self.cmd_list[2])

    def sleep(self):
        '''/sleep <sleep/wake> # sleep停止运动且不在执行/move指令'''
        self.sleep_or_wake = self.cmd_list[1]
        if self.cmd_list[1] == 'sleep':
            control.set_motor('0', '0')
    
    def setcolor(self):
        '''/setcolor <r> <g> <b> # 设置ws2812颜色'''
        WS2812.setColor(self.cmd_list[1], self.cmd_list[2], self.cmd_list[3])
        self.ws2812_color = self.cmd_list[1:]

    def name(self):
        '''/name <bot名> # 设置bot名'''
        self.bot_name = self.cmd_list[1]
        config_dict['bot_name'] = self.cmd_list[1]
        save_()
        
    
    def show(self):
        '''/show # 发送bot信息到udp客户端'''
        data = f'name:{self.bot_name}\nsleep or wake:{self.sleep_or_wake}\ncolor:{self.ws2812_color}\nteam:{self.bot_team}\n'
        send2wifi(data)
    
    def team(self):
        '''/team <队伍名> # 设置bot队伍'''
        self.bot_team = self.cmd_list[1]
        config_dict['team'] = self.cmd_list[1]
        save_()

    def randomcolor(self):
        '''/randomcolor # 随机颜色'''
        WS2812.random_color()

bot = cmd() # 创建机器人命令处理


def set_password(ssid_, password_):
    global SSID, PASSWORD
    SSID, PASSWORD = ssid_, password_
    
def creat_bot(name, team):
    '''创建机器人信息'''
    global bot
    bot.bot_name = name
    bot.bot_team = team

def connectWifi(ssid,passwd): 
    '''链接WiFi'''  
    global wlan
    wlan = network.WLAN(network.STA_IF) 
    wlan.active(True)   #激活网络
    wlan.disconnect()   #断开WiFi连接
    wlan.connect(ssid, passwd)   #连接WiFi
    while(wlan.ifconfig()[0] == '0.0.0.0'):   #等待连接
        time.sleep(1)
    print('network config:', wlan.ifconfig())
    WS2812.setColor(255, 255, 0)
    return True

def send2wifi(data):
    '''通过TCP发送信息'''
    global ret, conn
    ret = conn.send(data)

def first_send_date():
    '''发送bot信息'''
    sleep(0.5)
    send2wifi('/infor' 
              +' '+ get_config_var()['aruco_id']
              +' '+ get_config_var()['bot_name']
              +' '+ get_config_var()['team'])
    WS2812.setColor(0, 0, 0)



creat_bot(get_config_var()['bot_name'], get_config_var()['team'])

def creat_server():
    '''建立TCP服务器'''
    global ret, conn, listenSocket, wlan, port, first_send
    connectWifi(SSID,PASSWORD)
    ip = wlan.ifconfig()[0]   #获取IP地址
    listenSocket = socket.socket()   #创建套接字
    listenSocket.bind((ip, port))   #绑定地址和端口号
    listenSocket.listen(1)   #监听套接字
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #设置套接字
    print ('tcp waiting...')

    while True:
        print("accepting.....")
        WS2812.setColor(0, 255, 0)
        conn, addr = listenSocket.accept()   #接收连接请求，返回收发数据的套接字对象和客户端地址
        print(addr, "connected")

        while True:
            data = conn.recv(1024)   #接收数据（1024字节大小）

            if first_send:
                first_send_date()
                first_send = 0

            if(len(data) == 0):   #判断客户端是否断开连接
                print("close socket")
                conn.close()   #关闭套接字
                break
            print(data)
            recv_data_str = data.decode("utf-8")
            if bot.input_(recv_data_str) is False:  # 判断是否为简单运动指令
                control.easy_move(recv_data_str)

if __name__=="__main__":
    if get_config_var()['wifi'] == 'on': #开启TCP线程
        _thread.start_new_thread(creat_server, ())
    
    while get_config_var()['main'] == 'on': #任务分配，进入core1 防止看门狗重启
        sleep(1)
