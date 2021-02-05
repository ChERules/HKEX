
# Project hkex.py
# support file: myfunctions.py
# by: Albert Lam <albert@lamfamily.hk>
#
import os
import datetime
import myfunctions as mf
import movingAverage as ma
import linearLeastSquare as lsq

# MAIN Function starts

#
# DOWNLOADING DAILY QUOTATION WEBPAGES FROM HONG KONG STOCK EXCHANGE
#
# create a string of today's date yymmdd format
now = datetime.datetime.now()
lst = str(now.year)[-2:]+('00'+str(now.month))[-2:]+('00'+str(now.day))[-2:]

# set up directories to store html and extracted data
wdir = os.getcwd()
hdir = wdir + '/HTML/'
ddir = wdir + '/Data/'
adir = wdir + '/Analysis/'
if not os.path.exists(hdir): os.mkdir(hdir)
if not os.path.exists(ddir): os.mkdir(ddir)

# Set up the starting date for the quotation wegpage download.
# 1. look for the last downloaded file date in env.text
# 2. check the list of html files already downloaded to determine the last day.
# 3. As a last resort set date to "190430" seems webpage before May 2019 is no
#    longer available.
fst = '190430'
os.chdir(hdir)

# the last date of webpage which was downloaded
if os.path.isfile('env.txt'):
    f = open('env.txt', 'r')
    for line in f:
        if line.startswith('lastdate'):
            fst = line[9:15]
            break
    f.close()
else:
    # retrun a list of filename without extention
    datelist = mf.extlist(hdir, '.html', 'N')
    if len(datelist) >= 1:
        datelist.sort()
        fst = datelist[len(datelist)-1]
# lastdate: the date which the webpage was successfully downloaded.
lastdate = fst

# try to download webpages between the last day and today
while fst < lst:

    fst = mf.nextday(fst)

    url = "https://www.hkex.com.hk/eng/stat/smstat/dayquot/d"+fst+"e.htm"
    fname = fst + '.html'
    tname = fst + '.txt'
    # download the page if it exists
    if mf.url_is_alive(url):
        print('Downloading : ', fname)
        mf.dnload(url, fname, tname)

        # delete the downloaded file which is too small to contain data
        finfo = os.stat(fname)
        if finfo.st_size < 1024:
            os.remove(fname)
            os.remove(tname)
        else:
            lastdate = fst

# record the last date which webpage was downloaded
f = open('env.txt','w')
f.write('lastdate:'+lastdate+'\n')
f.close()

#
# EXTRACT THE SUMMARY OF THE DAILY ACTIVITY FROM EACH DOWNLOADED WEBPAGE
# OF EACH STOCK AND SAVE IT IN "quotations.csv"
#
os.chdir(ddir)
# READ WHAT HAS BEEN DONE PREVIOUSLY TO AVOID REPEATITION
# retrive a list of files in HTML directory and sorted them
hfiles = mf.extlist(hdir, '.html', 'Y')
hfiles.sort()

# create a company database if it doesn't exists
if not os.path.isfile('company.csv'): mf.crcof()

# create a list of company already in the company.csv file
clist = []
cfile = open('company.csv', 'r')
for line in cfile:
    if line.startswith('code'): continue
    co = line.split(',')
    clist.append(co[0])
cfile.close()

# list of trading date which result had been read previously
dlist = dict()
if os.path.isfile('sessions.csv'):
    sfile = open('sessions.csv', 'r')
    for line in sfile:
        if line.startswith('date'): continue
        sn = line.split(',')
        dlist[sn[0]] = sn[2].strip()
    sfile.close()
    os.remove('sessions.csv')

# create the quotations.csv file if doesn't exists
if not os.path.isfile("quotations.csv"):
    fout = open('quotations.csv', 'w')
    fout.write('code,date,tdn,high,low,close,ask,bid,turnover,volume\n')
    fout.close()

# create a new sessions file for this session.
sfile = open('sessions.csv', 'w')
sfile.write('date,idx,tdnum\n')

# loop throught all the downloaded webpages
for file in hfiles:
    # extract the date and its order among all webpages
    # hfiles already sorted previously
    date = file[:6]
    idx = str(hfiles.index(file))

    # if page already been read previously, record it and preceed to next page.
    if date in dlist:
        sfile.write(date+','+idx+','+dlist[date]+'\n')
        continue
    else:
        # extract the data and add it to the "quotations.csv"
        print('Processing : ', file)
        tdn = mf.read_h(hdir+file, clist)
        # record the files has been processed before move on to next one
        sfile.write(date+','+idx+','+tdn+'\n')

sfile.close()

#
#  EXACT DATA OF COMPANY OF INTEREST AND SAVE IT IN AN INDIVIDUAL CSV FILE
#
# setup lower, upper and increament for moving average and linear least linearLeastSquare
range = {'lower':5,'upper':50,'skip':5} # lower, upper and inc
# gather a list of company which we have data on file
cinfo = dict()
cfile = open('company.csv', 'r')
for line in cfile:
    if line.startswith('code'):
        continue
    else:
        c = line.split(',')
        cinfo[c[0]] = c[1]+' ('+c[2]+')'
cfile.close()

# ask user the stock code of all the companies they are inteested in
colist = []
code = '0'
while not code == 'q':
    print('\nWhat is the stock code of the company you want me to extract? ')
    code = input('Enter code or q to quite: ')
    # exit if answer is 'q'
    if code == 'q':
        continue
    # confirm with user and extract the data if code is in database
    elif code in cinfo:
        print('\nCompany with code: ', code, ' is ', cinfo[code])
        ans = input('Is it correct? (y/n): ')
        if ans == 'y':
            colist.append(code)
            t = input('\nDo you want me to prepare data for another company? (y/n): ')
            if t == 'n': code = 'q'
        else:
            print("\nLet's try again.\n")
    # ask for another code if it is not on record
    else:
        print('\nSorry, code is not in my record. Please try again.')

# SETTING UP Enviroments
if not os.path.exists(adir): os.mkdir(adir)

for code in colist:
    mf.csv(code)
    ma.mvavg(code,ddir,adir,range)
    lsq.llsq(code,ddir,adir,range)

# inform user where to expect the data file is located
print('\nThe data you need should be in located in ', adir)
