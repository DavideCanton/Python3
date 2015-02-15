import math

h1w = .1
h1wb = .1
yh1w = .1
ywb = .1
eps = .5
t = 100000

print("Faccio", t, "epoche\n")
func = math.sin
dd = list(map(func, range(10)))
x = dd[:]

for n in range(t):
    for i in range(len(x)):

        ah = x[i] * h1w + h1wb
        h = 1.0 / (1 + math.exp(-ah))
        ay = h * yh1w + ywb
        y = 1.0 / (1 + math.exp(-ay))
        erry = dd[i] - y
        dy = erry * y * (1 - y)
        errh = dy * yh1w
        dh = errh * h * (1 - h)
        h1w += eps * dh * x[i]
        h1wb += eps * dh
        yh1w += eps * dy * h
        ywb += eps * dy

print("h1w =", h1w)
print("h1wb =", h1wb)
print("yh1w =", yh1w)
print("ywb =", ywb, "\n")

for i in range(len(x)):
    ah = x[i] * h1w + h1wb
    h = 1.0 / (1 + math.exp(-ah))
    ay = h * yh1w + ywb
    y = 1.0 / (1 + math.exp(-ay))
    print(x[i], "->", y, "/", dd[i], "Errore: ",
          "%1.2f%%" % (math.fabs(dd[i] - y) * 100))
