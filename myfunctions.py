import os
import urllib.request

def crcof():
    # create a company profile csv file
    fout = open('company.csv','w')
    fout.write('code,name,cur,outstanding,added\n')
    fout.close()

def extlist(path, ext, w):
    # create a list of files in path with extention ext
    # path : str of path to search
    # ext : str of extention of files to be search
    # w : if 'Y', returen a list file names with extention
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

def url_is_alive(site):
    # check HTML's header to make sure the URL is valid

    request = urllib.request.Request(site)
    request.get_method = lambda: 'HEAD'

    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False

def dnload(site, fname):
    f, headers = urllib.request.urlretrieve(site)
    qpage = open(f)
    g = open(fname, 'w')
    for line in qpage:
        g.write(line)
    g.close()
    qpage.close()

def read_line(t):
    r = []
    if t.find('&amp;') > -1:
        t = t.replace('&amp;', '&')
    if t.find("</font></pre><pre><font size='1'>") > -1:
        t = t.replace("</font></pre><pre><font size='1'>", "")
    if t.find('/') > -1:
        t = t.replace('/', ' ')
    r.append(t[1:6].strip())
    r.append(t[7:23].strip())
    r.append(t[24:27].strip())
    r.append(t[28:36].strip().replace(',', ''))
    r.append(t[37:45].strip().replace(',', ''))
    r.append(t[46:54].strip().replace(',', ''))
    r.append(t[55:].strip().replace(',', ''))
    return(r)

def read_h(html, co):
    td = html[-11:-5]
    out = 'quotations.csv'
    qpage = open(html, 'r')

    st = 's'

    for line in qpage:
        if line.strip() == '': continue
        # search the session number and date
        if st == 's':
            if line.find(td) > -1:
                line = "00" + line
                senum = line[:line.index('/')]
                senum = senum[-3:]
                qout = open(out, 'a')
                st = 'h'
        # locate the beginning of the quotation section
        elif st.startswith('h'):
            if line.find('<a name = "quotations">QUOTATIONS</a>') > -1:
                st = 'h1'
            elif line.find('CODE') and st == 'h1':
                st = 'h2'
            elif line.find('CLOSING') and st == 'h2':
                st = 'q'
        # read the first line of each quotation
        elif st == 'q':
            # stop the reading operation once the end of section is reached
            if line.startswith('------'):
                qout.close()
                st = 'd'
                break
            q = read_line(line)
            #print(q[0])
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
                csvout = code + ',' + td + ',' + senum+','
                csvout = csvout + high + ',' + low + ',' + close + ','
                csvout = csvout + ask + ',' + bid + ',' + tunovr + ','
                csvout = csvout + traded + '\n'
                qout.write(csvout)
    return(senum)

def llsq(x,y):
    # Perform lineer least square fittinog over the data points
    # return a list with slope and y-intercept if successful
    # return 'fail' if determinant = 0
    # points : a list of coordinates of data points
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
