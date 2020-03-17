def myg ():
    a = 1
    while True:
        a += 1
        yield a


q=100
for i in myg():
    print (i)
    q -= 1
    if q < 0:
        break