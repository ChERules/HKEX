import os
import myfunctions as mf
wdir = os.getcwd()
hdir = wdir + '/HTML/'
os.chdir(hdir)
htmllist = mf.extlist(hdir, '.html', 'N')
for fst in htmllist:
    fname = fst + '.html'
    tname = fst + '.txt'
    print('processing', fname)
    mf.html2txt(fname, tname)
