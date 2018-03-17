import os
import datetime
import myfunctions as mf

# MAIN Function starts
now = datetime.datetime.now()
lst = str(now.year)[-2:]+('00'+str(now.month))[-2:]+('00'+str(now.day))[-2:]

wdir = os.getcwd()
hdir = wdir + '/HTML/'
ddir = wdir + '/Data/'

if not os.path.exists(hdir): os.mkdir(hdir)
if not os.path.exists(ddir): os.mkdir(ddir)

os.chdir(hdir)
datelist = mf.extlist(hdir, '.html', 'N')

fst = '170701'
if os.path.isfile('env.txt'):
	f = open('env.txt', 'r')
	for line in f:
		if line.startswith('lastdate'):
			fst = line[9:15]
			break
	f.close()
else:
	datelist.sort()
	fst = datelist[len(datelist)-1]

while fst <= lst:

	if not fst in datelist:
		url = "https://www.hkex.com.hk/eng/stat/smstat/dayquot/d"+fst+"e.htm"
		fname = fst + '.html'
		if mf.url_is_alive(url):
			print('Downloading : ', fname)
			mf.dnload(url, fname)
			finfo = os.stat(fname)
			if finfo.st_size < 1024:
				os.remove(fname)
			else:
				lastdate = fst

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

f = open('env.txt','w')
f.write('lastdate:'+lastdate+'\n')
f.close()

os.chdir(ddir)
#
# READ WHAT HAS BEEN DONE PREVIOUSLY TO AVOID REPEATING PAST EFFORTS
#
# retrive a list of files in HTML directory and sorted them
hfiles = mf.extlist(hdir, '.html', 'Y')
hfiles.sort()

# create a company database if it is not in the data directory already
if not os.path.isfile('company.csv'): mf.crcof()

# create a list of company already in the company.csv file
clist = []
cfile = open('company.csv', 'r')
for line in cfile:
	if line.startswith('code'): continue
	co = line.split(',')
	clist.append(co[0])
cfile.close()

# list of trading date which result had been read previously and delete previous sessions file
dlist = dict()
if os.path.isfile('sessions.csv'):
	sfile = open('sessions.csv', 'r')
	for line in sfile:
		if line.startswith('date'): continue
		sn = line.split(',')
		dlist[line[0]] = line[2].strip()
	sfile.close()
	os.remove('sessions.csv')

if not os.path.isfile("quotations.csv"):
	fout = open('quotations.csv', 'w')
	fout.write('code,date,tdn,high,low,close,ask,bid,turnover,volume\n')
	fout.close()
#
# PREPARING OUTPUT FILES TO ACCEPT NEW DATA
#
# create a new sessions file for this session.
sfile = open('sessions.csv', 'w')
sfile.write('date,idx,tdnum\n')

# open comapny.csv for more company entries
#cfile = open('company.csv', 'a')

# Extract records from each quotation csv file and write it to output file
for file in hfiles:
	date = file[:6]
	idx = str(hfiles.index(file))

	# sfile.write(date+','+idx+','+tdn+'\n')

	if date in dlist:
		sfile.write(date+','+idx+','+dlist[date]+'\n')
		continue
	else:
		print('Processing : ', file)
		tdn = mf.read_h(hdir+file, clist)
	sfile.write(date+','+idx+','+tdn+'\n')

sfile.close()
