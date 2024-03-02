def op(x,y,a,b):
    if x != a or y != b :
        x = a
        y = b
    return x, y

lx = 0
ly = 1
a = 1
b = 1

lx, ly = op(lx, ly, a, b)
print(lx, ly)