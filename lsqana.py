cc = '5'
apt = './Analysis/'
dpt = ''
inp = apt + cc + 'llsq.csv'
oup = apt + cc + 'lsqana.csv'

# prepare the header of the output file [0] [4]
inf = open(inp, 'r')
l = inf.readline()
ol = 'date,close,'

# extract all header starting with llsqc
while l.find('llsqc') > -1:
    l = l[l.index('llsqc'):]
    if l.find(',') > -1:
        ol = ol + l[:l.index(',')+1]
        l = l[l.index(',')+1:]
    else:
        ol = ol + l.strip()
        l = l[4:]
ol = ol + '\n'

ouf = open(oup, 'w')
ouf.write(ol)

ln = []    # for data in previous line
prj = []    # for storing previous predictions
ol = ''    # for formating projection output line

l = inf.readline()
ln = l.strip().split(',')
lth = len(ln)
ol = '{0[0]},{0[4]}\n'.format(ln)
ouf.write(ol)

for l in inf:
    ln = l.strip().split(',')

# format the output string by combining the current closing value and the previous predictions
    i = 0
    ol = ''
    while i < len(prj):
        ol = ol + ',{:.3f}'.format(prj[i])
        i = i + 1
    ol = '{0[0]},{0[4]}'.format(ln) + ol + '\n'
    ouf.write(ol)

    ct = (len(ln) - lth) // 3
    i = 0
    prj = []
    while i < ct: # and (len(ln2) > (lth * i + 6) ):
        po = lth + 2 + (i * 3)
        sl, yi = ln[po].split('/')
        nt = float(sl) * 101 + float(yi)
        prj.append(nt)
        i = i + 1

i = 0
ol = ','
while i < len(prj):
    ol = ol + ',{:.3f}'.format(prj[i])
    i = i + 1
ouf.write(ol+'\n')

ouf.close()
inf.close()
