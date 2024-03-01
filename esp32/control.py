from machine import Pin, PWM

MR = PWM(Pin(4, Pin.OUT), freq=1000)
ML = PWM(Pin(17, Pin.OUT), freq=1000)
ML.duty(0)
MR.duty(0)

def easy_move(s):
    # 用于调试
    if s == 'w':
        MR.duty(500)
        ML.duty(500)
    if s == 'a':
        MR.duty(500)
        ML.duty(0)
    if s == 'd':
        ML.duty(500)
        MR.duty(0)
    if s == 's':
        MR.duty(0)
        ML.duty(0)

def set_motor(pwmL,pwmR):
    global ML, MR
    MR.duty(int(pwmR))
    ML.duty(int(pwmL))