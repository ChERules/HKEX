# mvayg.py : moving average calculation
# by: Albert Lam

# assume conditions

import os
import myfunctions as mf



def llsq(cc,dph,aph):
    # cc = input('Enter the company code you want to calculate the moving average: ')
    # cc = cc.strip()
    #
    din = dph + cc + '.csv'
    inp = aph + cc + 'llsq.csv'
    oup = aph + cc + 'tmp.csv'

    inf = open(din, 'r')
    ouf = open(inp, 'w')
    l = inf.readline()
    l = l[l.index('date'):l.index(',ask')]+'\n'
    ouf.write(l)
    t = []
    for l in inf:
        t = l.split(',')
        l = '{0},{1},{2},{3},{4}\n'.format(t[1],t[2],t[3],t[4],t[5])
        ouf.write(l)
    inf.close()
    ouf.close()

    mvd = 5     # number of data point at start fitting
    inc = 5     # increment of number of data points
    lmt = 50    # maximum of data points to be used

    while mvd < lmt:
        # populate list of x value wiht last date as 100
        tmp = 100 - mvd + 1
        x = []
        while tmp <= 100:
            x.append(tmp)
            tmp = tmp + 1

        # prepare output file with header for each iteration
        inf = open(inp, 'r')
        l = inf.readline()	# read header
        ouf = open(oup, 'w')
        smvd = str(mvd)
        l = l.strip()+ ',llsqh'+smvd+ ',llsql'+smvd+ ',llsqc'+smvd+'\n'
        ouf.write(l)	# write header

        # initialize the list of high low, close value before the iteration
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

        # start the iteration by adding the last date's data to the list to calculate the least square fitting of the data set
        for l in inf:
            t = l.split(',')
            valh.append(float(t[2]))
            vall.append(float(t[3]))
            valc.append(float(t[4]))

            # calculat the lest square fitting and record the result
            lhigh = []
            llow = []
            lclose = []
            lhigh = mf.llsq(x,valh)
            llow = mf.llsq(x,vall)
            lclose = mf.llsq(x,valc)
            llsqh = '{0[0]:.3f}/{0[1]:.3f}'.format(lhigh)
            llsql = '{0[0]:.3f}/{0[1]:.3f}'.format(llow)
            llsqc = '{0[0]:.3f}/{0[1]:.3f}'.format(lclose)

            l = l.strip() + ',{0:s},{1:s},{2:s}\n'.format(llsqh, llsql, llsqc)
            ouf.write(l)
            # remove the oldest date high low close data point prepare for next iteration.
            valh.pop(0)
            vall.pop(0)
            valc.pop(0)
        ouf.close()
        inf.close()
        mvd = mvd + inc
        os.remove(inp)
        # if needed, add check to make sure inp is deleted before rename op.
        os.rename(oup, inp)
