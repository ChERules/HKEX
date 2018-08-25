# mvayg.py : moving average calculation
# by: Albert Lam

# assume conditions

import os
import myfunctions as mf

def mvavg(cc,ddir,adir):
    #   CALCUOLATING MOVING AVERAGES
    #
    # Set to calulate the moving average starting with 5 days data and wihh
    # increment of 5 days till the tartget maxium date average is reached.
    malow = 5
    mvd = malow # lower limits of moving data points
    maup = 50   # upper limit of moving average datapoints
    inc = 5     # increment

    din = ddir + cc + '.csv'
    inp = adir + cc + 'mvg.csv'
    oup = adir + cc + 'tmp.csv'

    # Collect the infromation and write it out to the output files
    # from the trade data collected from the .csv
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

    while mvd < maup:
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
        normal = True
        while c < (mvd - 1):
            l = inf.readline()
            if len(l) > 1:
                ouf.write(l)
                t = l.split(',')
                valh.append(float(t[2]))
                vall.append(float(t[3]))
                valc.append(float(t[4]))
                c = c + 1
            else:
                normal = False
                break

        if normal:
            for l in inf:
                t = l.split(',')
                valh.append(float(t[2]))
                vall.append(float(t[3]))
                valc.append(float(t[4]))
                avgh = mf.avg(valh)
                avgl = mf.avg(vall)
                avgc = mf.avg(valc)
                l = l.strip() + ',{0:.3f},{1:.3f},{2:.3f}\n'.format(avgh,avgl,avgc)
                ouf.write(l)
                valh.pop(0)
                vall.pop(0)
                valc.pop(0)
            ouf.close()
            inf.close()
            mvd = mvd + inc
            os.remove(inp)
            while os.path.isfile(inp): continue
            os.rename(oup, inp)
        else:
            maup = mvd
            ouf.close()
            inf.close()
            os.remove(oup)
    #
    #   EVALUATE AND ANALIZING THE CALCULATED MOVING AVERAGE
    #
    oup = adir + cc + 'mvana.csv'

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
            lo = lo + ',{0:.3f},{1:.3f},{2:.3f}'.format(ph,pl,pc)
            rn = rn + 1
        if len(lo) > 0:
            lo = '{0},{1:.3f}'.format(mv3[0],rt)+lo+'\n'
            ouf.write(lo)
        mv1 = mv2
        mv2 = mv3
    ouf.close()
    inf.close()
