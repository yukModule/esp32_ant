from machine import Pin
from utime import sleep_us, sleep
 
# 定义红外发射模块的引脚
ir_pin = Pin(26, Pin.OUT)

def carrier1(t):
    '''高位pwm 38kHz'''
    for _ in range(t):
        ir_pin.on()
        sleep_us(13)
        ir_pin.off()
        sleep_us(13)

def carrier0(t):
    '''低位'''
    sleep_us(26*t)

def r0():
    '''bit0 高位0.56ms+低位0.56ms'''
    carrier1(22)
    carrier0(21)

def r1():
    '''bit0 高位0.56ms+低位1.69ms'''
    carrier1(22)
    carrier0(65)

def ascii_2_list_bin(s):
    '''ascII转列表型8位二进制'''
    b = '{:08b}'.format(ord(s))
    return [ int(b[_]) for _ in range(8)]

def emit_ir(code):
    '''报文格式：
    - 前导码 9ms高位+4.5ms低位 
    - 数据码 8位数据
    - 校验码 8位数据反码
    - 截止码 1位0'''
    global r0, r1
    r_code = [r0, r1]
    # 前导码
    carrier1(346)
    carrier0(171)

    # 数据码
    for i in code:
        r_code[i]()
    # 校验码
    for i in code:
        r_code[1-i]()
    # 截止码
    r_code[0]()

# 发射红外信号
while True:
    emit_ir(ascii_2_list_bin('b'))
    sleep(1)
