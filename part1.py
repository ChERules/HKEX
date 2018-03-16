import os
import myfunctions as mf
# MAIN Function starts
fst = input('Enter starting date as "yymmdd" : ')
lst = input('Enter the last date as "yymmdd" : ')

fst = fst + "111111"
fst = fst[:6]
lst = lst + "111111"
lst = lst[:6]
wdir = os.getcwd()
hdir = wdir + '/HTML/'
ddir = wdir + '/Data/'

os.chdir(hdir)
datelist = []
for file in os.listdir():
	datelist.append(file[:6])

while fst <= lst:

	if not fst in datelist:
		url = "https://www.hkex.com.hk/eng/stat/smstat/dayquot/d"+fst+"e.htm"
		print("Processing", fst)
		fname = fst + '.html'
		if mf.url_is_alive(url):
			mf.dnload(url, fname)
			finfo = os.stat(fname)
			if finfo.st_size < 1024: os.remove(fname)

	yy = int(fst[:2])
	mm = int(fst[2:4])
	dd = int(fst[4:])
	dd = dd + 1
	if dd > 31:
		mm = mm + 1
		dd = 1
	if mm > 12:
		yy = yy + 1
		mm = 1

	fst = str('00'+str(yy))[-2:]+("00" + str(mm))[-2:]+("00" + str(dd))[-2:]
