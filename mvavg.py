# mvayg.py : moving average calculation
# by: Albert Lam

# assume conditions

import os

def avg(v):
    sum = 0.0
    for i in v:
        sum = sum + i
    avg = sum/len(v)
    return(avg)

dph = './Data/'
aph = './Analysis/'
if not os.path.exists(aph): os.mkdir(aph)
# cc = input('Enter the company code you want to calculate the moving average: ')
# cc = cc.strip()
#
cc = '5'
din = dph + cc + '.csv'
inp = aph + cc + 'mvg.csv'
oup = aph + cc + 'tmp.csv'

inf = open(din, 'r')
ouf = open(inp, 'w')
l = inf.readline()
l = l[l.index('date'):l.index(',ask')]+'\n'
ouf.write(l)
t = []
for l in inf:
    t = l.split(',')
    l = '{},{},{},{},{}\n'.format(t[1],t[2],t[3],t[4],t[5])
    ouf.write(l)
inf.close()
ouf.close()

mvd = 5
while mvd < 50:
    inf = open(inp, 'r')
    l = inf.readline()	# read header
    ouf = open(oup, 'w')
    smvd = str(mvd)
    l = l.strip() + ',mavgh'+smvd + ',mavgl'+smvd + ',mavgc'+smvd+'\n'
    ouf.write(l)	# write header

    valh = []
    vall = []
    valc = []
    c = 0
    while c < (mvd - 1):
        l = inf.readline()
        ouf.write(l)
        t = l.split(',')
        valh.append(float(t[2]))
        vall.append(float(t[3]))
        valc.append(float(t[4]))
        c = c + 1

    for l in inf:
        t = l.split(',')
        valh.append(float(t[2]))
        vall.append(float(t[3]))
        valc.append(float(t[4]))

        avgh = avg(valh)
        avgl = avg(vall)
        avgc = avg(valc)

        l = l.strip() + ',{0:.3f},{1:.3f},{2:.3f}\n'.format(avgh,avgl,avgc)
        ouf.write(l)
        valh.pop(0)
        vall.pop(0)
        valc.pop(0)
    ouf.close()
    inf.close()
    mvd = mvd + 5
    os.remove(inp)
    os.rename(oup, inp)
