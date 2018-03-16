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

os.chdir(ddir)
#
# READ WHAT HAS BEEN DONE PREVIOUSLY TO AVOID REPEATING PAST EFFORTS
#
# retrive a list of files in HTML directory and sorted them
hfiles = mf.extlist(hdir, '.html', 'Y')
hfiles.sort()

# retrive a list of files in dataset director
dfiles = mf.extlist(ddir, '.csv', 'Y')

# create a company database if it is not in the data directory already
if not 'company.csv' in dfiles: mf.crcof()

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
if 'sessions.csv' in dfiles:
	sfile = open('sessions.csv', 'r')
	for line in sfile:
		if line.startswith('date'): continue
		sn = line.split(',')
		dlist[line[0]] = line[2].strip()
	sfile.close()
	os.remove('sessions.csv')

if not "quotations.csv" in dfiles:
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
		tdn = mf.read_h(hdir+file, clist)
	sfile.write(date+','+idx+','+tdn+'\n')

sfile.close()
