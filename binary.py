import random


data = [random.randint(0, 1) for i in xrange(100)]
data.sort()


_from = 0
to = len(data)
delim = (to - _from) / 2

while not (data[delim] == 1 and data[delim-1] == 0):
    if data[delim] == 1:
        to = delim
        delim -= (to - _from) / 2
    elif data[delim] == 0:
        _from = delim
        delim += (to - _from) / 2

print delim, data[:delim], data[delim:]
