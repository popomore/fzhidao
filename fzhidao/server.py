from pyquery import PyQuery as pq
import time
import sys
import re
import urllib
import logging
import codecs

log = logging.getLogger()
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('[%(levelname)s] %(funcName)s: %(message)s'))
log.addHandler(ch)

a=[]
result=[]
datetime2=''
output = codecs.open('result.csv', 'w', encoding='utf-8') 

def fetch(i, o):
    try:
        link = pq(o).find('a').attr('href')
        date = pq(o).find('.lklbe').text()
        date = re.sub(r'\n',r'',date)
        date = re.sub(r'.*(\d{4}-\d{1,2}-\d{1,2}).*',r'\1',date)
        datetime1 = time.strptime(date,'%Y-%m-%d')
        if datetime1 > datetime2:
            log.debug('add' + date)
            a.append((link,date))
    except:
        log.error('fetch error')
        pass

def parse(d):
    tdlist = d('td.f')
    if tdlist:
       tdlist.map(fetch) 
       return True
    else:
       log.error('parse error')
       return False
        

def main():

    param1 = urllib.quote(sys.argv[1].decode('utf-8').encode('gbk'))
    if len(sys.argv) >= 3:
        try:
            global datetime2
            datetime2 = time.strptime(sys.argv[2],'%Y-%m-%d')
        except:
            datetime2 = time.strptime('1970-1-1','%Y-%m-%d')
            pass
    else:
        log.info('no parameter "date"')
        datetime2 = time.strptime('1970-1-1','%Y-%m-%d')
    
    
    for i in range(0,1000,10):
        url = 'http://zhidao.baidu.com/q?ct=17&tn=ikaslist&word='+param1+'&pn='+str(i) 
        try:
            zhidaolist = urllib.urlopen(url)
        except:
            log.error('get error ' + url)
            continue
        if(zhidaolist.getcode() == 200):
            log.info('get 200 ' + url)
            content = zhidaolist.read().decode('gbk')
        else:
            log.error('404')
            continue

        d = pq(content)   
        if parse(d):
            pass
        else:
            log.info('end at ' + str(i))
            break 

    for i, element in enumerate(a):
        log.debug(element)
        iurl = 'http://zhidao.baidu.com'+element[0]
        if not element[0]:
            continue
        try:
            zhidaolist = urllib.urlopen(iurl)
        except:
            log.error('get error ' + iurl)
            continue
        if(zhidaolist.getcode() == 200):
            log.info('parsing 200 ' + iurl)
            content = zhidaolist.read().decode('gbk')
            d = pq(content)
            title = d('h1#question-title').text()
            name = d('#question-box .user-name').text()
            date = element[1]
            cont = d('#question-content').text()
            try:
                cont = re.sub(r'\n',r' ',cont)
            except:
                log.error('parse error')
                pass
            r = "%s | %s | %s | %s | %s\n" % (title, name, date, iurl, cont)
            log.debug(r)
            output.write(r)
        else:
            log.error('404')
        pass

    output.close()
    
if __name__ == "__main__":
    main()

