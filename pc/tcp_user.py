import socket
from threading import Thread
from time import sleep

class tcp_user:
    def __init__(self,ip,bot_name):
        '''
        初始化
        - ip地址
        - 客户端名
        - 连接服务器
        '''
        self.tcp_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcp_client.connect((ip,7788))
        self.bot_name = bot_name
        pass

    def send_data(self,data):
        '''发送数据'''
        send_data = data.encode(encoding='utf-8')
        try:
            self.tcp_client.send(send_data)
        except:
            pass
    
    def listen_(self):
        '''循环监听'''
        while True:
            recv_data = self.tcp_client.recv(1024)
            print(self.bot_name,':', recv_data.decode(encoding = 'utf-8'))

    def thread_listen(self):
        '''开启多线程监听'''
        t1 = Thread(target=self.listen_)
        t1.start()

    def send_pass(self):
        '''防esp32看门狗'''
        def sthread_pass():
            while True:
                self.send_data('pass')
                sleep(2)

        t2 = Thread(target=sthread_pass)
        t2.start()



