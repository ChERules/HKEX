cc = '5'
apt = './Analysis/'
inp = apt + cc + 'mvg.csv'
oup = apt + cc + 'mvana.csv'

inf = open(inp, 'r')
l = inf.readline()
l = 'date,change'+ l[l.index(',mavg'):]
ouf = open(oup, 'w')
ouf.write(l)

mv1 = []
mv2 = []
mv3 = []

l = inf.readline()
mv1 = l.strip().split(',')
l = inf.readline()
mv2 = l.strip().split(',')

for l in inf:
    mv3 = l.strip().split(',')
    ct = (len(mv2) - 5) // 3
    lo = ''
    rn = 0
    rt = (float(mv3[4]) - float(mv2[4]))
    while (rn <= ct) and (len(mv1) > (3 * rn + 6) ):
        po = 2 + rn * 3
        ph = float(mv2[po]) - float(mv1[po])
        pl = float(mv2[po+1]) - float(mv1[po+1])
        pc = float(mv2[po+2]) - float(mv1[po+2])
        #ph = str(int(ph/abs(ph)))
        #pl = str(int(pl/abs(pl)))
        #pc = str(int(pc/abs(pc)))
        lo = lo + ',{0:.3f},{1:.3f},{2:.3f}'.format(ph,pl,pc)
        rn = rn + 1
    if len(lo) > 0:
        lo = '{0},{1:.3f}'.format(mv3[0],rt)+lo+'\n'
        ouf.write(lo)
    mv1 = mv2
    mv2 = mv3
ouf.close()
inf.close()
