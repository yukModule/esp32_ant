import neopixel
from machine import Pin
import urandom

LED = neopixel.NeoPixel(pin=Pin(12), n=1, timing=1)  # 创建控制对象

def setColor(r, g, b):
    '''设置ws2812颜色'''
    global LED
    LED.fill((int(r), int(g), int(b)))  # GRB填充数据(RGB顺序, 0为不亮，255为全亮)
    LED.write()  # 写入数据

def random_color():
    '''随机ws2812颜色'''
    r = urandom.randint(0, 255)
    g = urandom.randint(0, 255)
    b = urandom.randint(0, 255)
    LED.fill((r, g, b))  # 依次设置LED灯珠的颜色
    LED.write()  # 写入数据
