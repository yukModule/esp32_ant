from tcp_user import tcp_user
from get_bot_ipv4 import get_ip ,scan_ip

scan_ip()
print(get_ip())

# # ------------修改ip------------
# p = tcp_user('192.168.137.109','yuk2')
# p.thread_listen()
# p.send_pass()

# # ------------回车------------
# while True:
#     i = str(input())
#     # 按回车发送
#     p.send_data(i)
#     print('ok')
