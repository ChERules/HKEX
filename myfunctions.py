import os
import urllib.request, urllib.parse, urllib.error
import re

def nextday(dt):
    # setup the next date to try
    yy = int(dt[:2])
    mm = int(dt[2:4])
    dd = int(dt[4:])
    dd = dd + 1
    if dd > 31:
        mm = mm + 1
        dd = 1
    if mm > 12:
        yy = yy + 1
        mm = 1
    nd = str('00'+str(yy))[-2:]+("00" + str(mm))[-2:]+("00" + str(dd))[-2:]
    return(nd)

def csv(code):
    """
    extract trade data of a company, code, from the master file
    quotations.csv and copy them to the file code.csv
    """
    if os.path.isfile(code+'.csv'): os.remove(code+'.csv')
    qr = open('quotations.csv', 'r')
    ou = open(code+'.csv', 'w')
    for line in qr:
        t1 = line.split(',')
        if t1[0] == code or t1[0] == 'code':
            ou.write(line)
    ou.close()
    qr.close()

def avg(v):
    """
    calculate the avage of the value in list v
    """
    sum = 0.0
    for i in v:
        sum = sum + i
    avg = sum/len(v)
    return(avg)

def crcof():
    # create a company profile csv file
    fout = open('company.csv','w')
    fout.write('code,name,cur,outstanding,added\n')
    fout.close()

def extlist(path, ext, w):
    """
    create a list of files in path with extention ext
    path : str of path to search
    ext : str of extention of files to be search
    w : if 'Y', returen a list of file names with extention
    """
    flist = []
    pos = len(ext)
    for file in os.listdir(path):
        if pos > 0:
            if file.endswith(ext):
                if w == 'Y':
                    flist.append(file)
                else:
                    flist.append(file[:-1*pos])
        else:
            flist.append(file)
    return(flist)

def url_is_alive(url):
    """
    Checks that a given URL is reachable.
    param url: A URL
    """
    try:
        urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        return False
    return True

def dnload(site, fname):
# Read the "site" and write it out to "fname"
# to preserve the original html file
# Then call html2txt to strip down the html tags.
    hl = urllib.request.urlopen(site).read().decode()
    fout = open(fname, 'w')
    fout.write(hl)
    fout.close()

def striptag(l):
    ln = l.rstrip()
    if len(ln) > 0:
        ln = re.sub('<.+?>', '', ln)
        if len(ln) > 0:
            schr = re.findall('&.+;', ln)
            if len(schr) > 0:
                for ch in schr:
                    if ch == '&amp;': ln = re.sub(ch, '&', ln)
                    elif ch == '&quot;': ln = re.sub(ch, '"', ln)
                    elif ch == '&lt;': ln = re.sub(ch, '<', ln)
                    elif ch == '&gt;': ln = re.sub(ch, '>', ln)
    return(ln)

def html2txt(html,txt):
# strip all html tags and convert '& sequences'
# save the text to a text file "tname" for easy reading
    h = open(html,'r')
    t = open(txt,'w')
    for l in h:
        ln = l.rstrip()
        if len(ln) > 0:
            ln = striptag(l)
        t.write(ln+'\n')
    t.close()
    h.close()

def read_line(t):
    r = []
    r.append(t[1:6].strip())
    r.append(t[7:23].strip())
    r.append(t[24:27].strip())
    r.append(t[28:36].strip().replace(',', ''))
    r.append(t[37:45].strip().replace(',', ''))
    r.append(t[46:54].strip().replace(',', ''))
    r.append(t[55:].strip().replace(',', ''))
    return(r)

def read_h(filename, co):
    td = filename[-11:-5]
    out = 'quotations.csv'
    qpage = open(filename, 'r')

    st = 's'

    for line in qpage:
        if line.strip() == '': continue
        # strip html tags and convert escape sequence
        line = striptag(line)
        # search and extract the session number for the year
        if st == 's':
            if line.find(td) > -1:
                line = "00" + line
                senum = line[:line.index('/')]
                senum = senum[-3:]
                qout = open(out, 'a')
                st = 'h'
        # locate the beginning of the quotation section
        elif st == 'h':
            if line.find('CLOSING      BID     LOW        TURNOVER ($)') > -1:
                st = 'q'
        # read the first line of each quotation
        elif st == 'q':
            # stop the reading operation once the end of section is reached
            if line.startswith('------'):
                qout.close()
                st = 'd'
                break
            q = read_line(line)
            if len(q[0]) > 0:
                code = q[0]
                name = q[1]
                cur  = q[2]
                prv  = q[3]
                ask  = q[4]
                high = q[5]
                traded = q[6]
                if not code in co:
                    cfile = open('company.csv', 'a')
                    cfile.write(code+','+name+','+cur+',,'+td+'\n')
                    co.append(q[0])
                    cfile.close()
            else:
                # read the next line of the quotation
                close = q[3]
                bid = q[4]
                low = q[5]
                tunovr = q[6]
                csvout = "{},{},{},{},{},{},{},{},{},{}\n".format(code,td,senum,high,low,close,ask,bid,tunovr,traded)
                qout.write(csvout)
    return(senum)

def llsqfit(x,y):
    """
    Perform lineer least square fittinog over the data points
    return a list with slope and y-intercept if successful
    return 'fail' if determinant = 0
    points : a list of coordinates of data points
    """
    n = len(x)
    sumx = 0.0
    sumy = 0.0
    sumxx = 0.0
    sumxy = 0.0

    # calculate the various sums from the data set
    count = 0
    while count < n:
        sumx = sumx + x[count]
        sumy = sumy + y[count]
        sumxx = sumxx + x[count]**2
        sumxy = sumxy + x[count]*y[count]
        count = count + 1

        # calculate the coeffient of the fitted line in the form of y = a + bx
    detern = n * sumxx - sumx**2
    if detern == 0:
        return('failed')
    else:
        yintc = (sumy * sumxx - sumx * sumxy)/detern
        slop = (n * sumxy - sumx * sumy)/detern
        return(slop,yintc)
