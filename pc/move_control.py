from visual_feedback import get_bot_posture, show_err
import bot_init as bot_
import contextlib
import math
from time import sleep

tick = 1
delay = 1 # 需要测试调试

def trim_cmd_and_send(motor_L,motor_R,bot_id):
    '''
    电机pwm 整理并发送
    /move motor_L motor_R
    '''
    bot_.set_cmdlist(['/send', bot_id, '/m', str(motor_L), str(motor_R)]) 
    bot_.send()

def send_optimize(bot_id, motor_L, motor_R, motor_L_l, motor_R_l):
    '''优化发送'''
    if motor_R != motor_R_l or motor_L != motor_L_l: 
        with contextlib.suppress(Exception): # 尝试发送
            trim_cmd_and_send(motor_L, motor_R, bot_id)
        motor_R_l = motor_R
        motor_L_l = motor_L
        sleep(0.1) # 等待机器人TCP中断处理
    return motor_L_l, motor_R_l

def get_angle(x1, y1, x2, y2):
    '''获取从当前点到目标点的向量角度'''
    return math.atan2((y2-y1),(x2-x1)) / math.pi * 180

def goal_now_posture(bot_id):
    '''获取当前位姿'''
    dic = get_bot_posture()
    now_x = dic[bot_id].x
    now_y = dic[bot_id].y
    now_angle = dic[bot_id].angle
    return now_x, now_y, now_angle


def forecast_angle(last_x, last_y, now_x, now_y, now_angle, x, y):
    '''预测角度'''
    global tick, delay
    v = math.sqrt( (last_x-now_x)**2 +(last_y-now_y**2) ) / tick
    next_x = v*delay*math.cos(math.radians(now_angle)) + now_x # 预测下一时刻坐标
    next_y = v*delay*math.sin(math.radians(now_angle)) + now_y

    angle_err = now_angle - get_angle(next_x, next_y, x, y) # 预测角度误差

    if angle_err < -180: # 最小偏差角 [-180, 180] angle_err>0 逆时针
        angle_err += 360
    if angle_err > 180:
        angle_err -= 360
    return angle_err, now_x, now_y, next_x, next_y

def rot_move(bot_id, a, c):
    '''令机器人朝向某角度a, 容许角度误差为c'''
    now_x, now_y, now_angle = goal_now_posture(bot_id)
    motor_R_l, motor_L_l = 0, 0
    a = int(a)
    c = int(c)
    while True:
        now_x, now_y, now_angle = goal_now_posture(bot_id) # 通过视觉获取机器人当前坐标
        angle_err = now_angle - a # 获取角度偏差
        if angle_err < -180: # 最小偏差角 [-180, 180]
            angle_err += 360
        if angle_err > 180:
            angle_err -= 360

        if angle_err<-1*c : 
            motor_L = 0
            motor_R = 500
        elif angle_err>c :
            motor_L = 500
            motor_R = 0

        else:
            break

        # 减轻服务器负担，提高相应速度，只有与上一次数据不同时才发送
        motor_L_l, motor_R_l = send_optimize(bot_id, motor_L, motor_R, motor_L_l, motor_R_l)

    sleep(0.1)
    trim_cmd_and_send(0, 0, bot_id)
    print(bot_id, '已到旋转到',a)
        
def rotp_move(bot_id, x, y, a):
    '''令机器人朝向某点, 容许角度误差为a'''
    now_x, now_y, now_angle = goal_now_posture(bot_id)
    motor_R_l, motor_L_l = 0, 0
    while True: #如果不在目标范围内 则执行
        now_x, now_y, now_angle = goal_now_posture(bot_id) # 通过视觉获取机器人当前坐标
        angle_err = now_angle - get_angle(now_x, now_y, x, y) # 获取角度偏差
        if angle_err < -180: # 最小偏差角 [-180, 180] angle_err>0 逆时针
            angle_err += 360
        if angle_err > 180:
            angle_err -= 360

        show_err(angle_err, now_x, now_y) # 在相机上显示

        # 使机器人朝向始终指向目标点
        if angle_err<-1*a : 
            motor_L = 0
            motor_R = 500
        elif angle_err>a :
            motor_L = 500
            motor_R = 0
        else:
            break

        # 减轻服务器负担，提高相应速度，只有与上一次数据不同时才发送
        motor_L_l, motor_R_l = send_optimize(bot_id, motor_L, motor_R, motor_L_l, motor_R_l)

    sleep(0.1)
    trim_cmd_and_send(0, 0, bot_id)
    print(bot_id, '已到指向', x, y)

def allowable_error(x1, y1, x2, y2, al_er):
    '''是否到达目标点位'''
    return (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) > al_er*al_er

# 有预测控制
def line_move(x,y,bot_id,a,r):
    '''直线运动到目标点'''
    global tick, delay
    now_x, now_y, now_angle = goal_now_posture(bot_id)
    motor_R_l, motor_L_l = 0, 0
    last_x, last_y = now_x, now_y
    r = int(r)
    a = int(a)
    while allowable_error(now_x, now_y, x, y, r): #如果不在目标范围内 则执行
        now_x, now_y, now_angle = goal_now_posture(bot_id) # 通过视觉获取机器人当前坐标

        # 预测
        angle_err, last_x, last_y, next_x, next_y = forecast_angle(last_x, last_y, now_x, now_y, now_angle, x, y)
        if allowable_error(next_x, next_y, x, y, r) == False:
            break

        show_err(angle_err, now_x, now_y) # 在相机上显示

        # 使机器人朝向始终指向目标点
        if angle_err<-1*a : 
            motor_L = 0
            motor_R = 500
        elif angle_err>a :
            motor_L = 500
            motor_R = 0
        else:
            motor_R = 500
            motor_L = 500

        # 减轻服务器负担，提高相应速度，只有与上一次数据不同时才发送
        motor_L_l, motor_R_l = send_optimize(bot_id, motor_L, motor_R, motor_L_l, motor_R_l)

    sleep(0.1)
    trim_cmd_and_send(0, 0, bot_id)
    print(bot_id, '已到达', x, y)

# 无预测控制
# def line_move(x,y,bot_id,a,r): 
#     '''直线运动到目标点'''
#     now_x, now_y, now_angle = goal_now_posture(bot_id)
#     motor_R_l, motor_L_l = 0, 0
#     r = int(r)
#     a = int(a)
#     while allowable_error(now_x, now_y, x, y, r): #如果不在目标范围内 则执行
#         now_x, now_y, now_angle = goal_now_posture(bot_id) # 通过视觉获取机器人当前坐标
#         angle_err = now_angle - get_angle(now_x, now_y, x, y) # 获取角度偏差
#         if angle_err < -180: # 最小偏差角 [-180, 180] angle_err>0 逆时针
#             angle_err += 360
#         if angle_err > 180:
#             angle_err -= 360

#         show_err(angle_err, now_x, now_y) # 在相机上显示

#         # 使机器人朝向始终指向目标点
#         if angle_err<-1*a : 
#             motor_L = 0
#             motor_R = 500
#         elif angle_err>a :
#             motor_L = 500
#             motor_R = 0
#         else:
#             motor_R = 500
#             motor_L = 500

#         # 减轻服务器负担，提高相应速度，只有与上一次数据不同时才发送
#         motor_L_l, motor_R_l = send_optimize(bot_id, motor_L, motor_R, motor_L_l, motor_R_l)

#     sleep(0.1)
#     trim_cmd_and_send(0, 0, bot_id)
#     print(bot_id, '已到达', x, y)