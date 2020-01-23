import math
from math import sin, cos, radians, atan2
x0 = 100
y0 = 100
x = x0 + 50 * sin(radians(90))
y = y0 + 50 * cos(radians(90))

print(x, y)


x1 = 100
x2 = 150
y1 = 100
y2 = 100
print(atan2(x2 - x1, y1 - y2) / math.pi * 180)


