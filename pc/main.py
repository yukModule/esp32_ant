from bot_init import cmd, init
from visual_feedback import task_open_vf

init() # 客户端初始化
task_open_vf() # 开启视觉反馈

while True:
    cmd(input())