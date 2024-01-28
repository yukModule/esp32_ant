from tcp_user import tcp_user
from get_bot_ipv4 import get_ip ,scan_ip

bot_num = 0

scan_ip()
print(get_ip())
bot_num = len(get_ip())

# 生成机器人对象
bot_list = [_ for _ in range(bot_num)] 
print(bot_list)

for i in range(bot_num):
    print('尝试建立连接',i,get_ip()[i])
    try:
        bot_list[i] = tcp_user(get_ip()[i],'yuk2')
        bot_list[i].thread_listen()
        bot_list[i].send_pass()
        print(i,get_ip()[i],'建立成功')
    except:
        print(i,get_ip()[i],'不可用或没有开启TCP服务器')

while True:
    pass
