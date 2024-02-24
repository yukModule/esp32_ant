from bot_init import cmd, init
from visual_feedback import task_open_vf

init()
task_open_vf()

while True:
    cmd(input())