import math

x1 = 0
y1 = 0

x2 = 1
y2 = 1

angle = math.atan2((y2-y1),(x2-x1)) / math.pi * 180 - 90

print(angle)