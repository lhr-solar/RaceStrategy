import math
N = (256 * 2.20462)
K = 2.47
d0 = 21.67
dw = 16
p = 75
p0 = 80
h = (0.5 * (d0/dw) * math.pow((p/p0), 0.3072) * \
                (dw - math.pow(math.pow(dw, 2) - (4 * N/math.pi) * \
                ((2.456 + 0.251 * dw) / (19.58 + 0.5975 * p)), 0.5)))
print(h)