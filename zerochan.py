#!/usr/bin/env python
# encoding: utf-8
# Example: python zerochan.py 'Tales of Zestiria'
import os
import re
import sys
import math
import random
import time
import requests
import lxml
from bs4 import BeautifulSoup
from os.path import join, getsize
import json

reload(sys)

log = open('log.txt','a')
links = open('links.txt','a+')
fsus = open('sus.txt','a+')
ffai = open('fail.txt','a+')
links.seek(0,0)
fsus.seek(0,0)
ffai.seek(0,0)

keyword = "Majo+no+Tabitabi"
url = 'https://www.zerochan.net/'
maxpage = 1
needpage = -1  #抓取前needpage页
link = set()
succes_link = set()
failed_link = set()
recaplink = True
download = True

cookies = ''


def login():
    global cookies
    headers = {
        'Origin': 'https://www.zerochan.net',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Referer': 'https://www.zerochan.net/login?ref=%2FShihou%2BMatsuri%3Fp%3D3',
    }

    data = {
      'ref': '/Shihou+Matsuri?p=3',
      'name': 'kanoto',
      'password': '767huanyu',
      'login': 'Login'
    }

    r = requests.post('https://www.zerochan.net/login', headers=headers, data=data)
    cookies = r.cookies
    print('cookies:')
    print(cookies)
    pass

def writeln(s):
    print s
    log.write(s + '\n')
    log.flush()
    pass

def getkeyword():
    if len(sys.argv)<=1:
        return keyword.replace(' ','+')
    tmp = sys.argv[1]
    for i in xrange(2,len(sys.argv)):
        tmp+='+'+sys.argv[i]
    writeln('Key word is \"%s\"'%(tmp))
    return tmp


def safe_request(url, cookies=''):

    pass


def dealLink(rawurl):
    imageurl = rawurl.strip().replace('s3','static').replace('.240.','.full.')
    print 'Real url is:',imageurl
    try:
        r = requests.get(imageurl, cookies=cookies)
        content = r.content
    except Exception as e:
        content = ''
    name = ''
    if len(content) < 10240:
        print len(content)
        return -1
    else:
        name = imageurl[imageurl.rfind('/')+1:]
    with open(name, "wb") as code:
        code.write(r.content)
    if name[-3:] == 'jpg':
        return 0
    elif name[-3:] == 'png':
        return 1
    else:
        print '2'
        return -1
    pass


if __name__ == '__main__':
    keyword = getkeyword()
    login()

    while True:
        j = fsus.readline().strip()
        if len(j)==0:
            break
        succes_link.add(j)
    while True:
        j = ffai.readline().strip()
        if len(j)==0:
            break
        failed_link.add(j)

    r = requests.get(url + keyword, cookies=cookies)
    # r = requests.get('https://www.zerochan.net/4K+Ultra+HD+Wallpaper?s=fav')

    s = r.text.encode('utf-8')
    print re.findall('page 1 of \d*',s)
    maxpage = int(re.findall('page 1 of \d*',s)[0][10:])
    writeln('A total of %d pages'%(maxpage))
    soup = BeautifulSoup(s,'lxml')
    keyword = soup.find_all(id='menu')[0].h2.string.encode('utf-8').replace(' ','+')
    print 'Real keyword is \"%s\"'%(keyword)

    if recaplink:
        payload = {'p':1}
        pre = 0
        for indx in range(1,maxpage+1):
            r = requests.get(url + keyword + '?p=%d'%(indx), cookies=cookies)
            s = r.text.encode('utf-8')
            # lst = re.findall('http.*\.240\..*\.jpg',s)
            lst = [i[len('"url": "'):-len('",')] for i in re.findall('"url":.+",',s)]
            for i in lst:
                link.add(i)
            writeln('Page %d finished, %d pictures added.'%(indx,len(link)-pre))
            pre = len(link)
        writeln('Link capture finished. %d pictures in all'%(len(link)))
        linkout = open('links.txt','w')
        for i in link:
            linkout.write(i + '\n')
        linkout.flush()
        linkout.close()
    else:
        while True:
            j = links.readline()
            if len(j)==0:
                break
            link.add(j)

    if download:
        foldername = keyword.replace('+',' ')
        if not os.path.exists(foldername):
            os.mkdir(foldername)
        os.chdir(foldername)
        loc = os.getcwd()
        tmp = 'Start downloading %d pictures. Save path is %s'%(len(link),loc)
        writeln(tmp)

        sus = 0
        fail = 0
        for i in link:
            if i in succes_link:
                sus += 1
                writeln('The pic downloaded before,ignore.\tNow sus:%5d,fail:%5d.'%(sus,fail))
                continue
            tmp = dealLink(i)
            if tmp >= 0:
                sus += 1
                succes_link.add(i)
                fsus.write(i + '\n')
                fsus.flush()
                if i in failed_link:
                    failed_link.remove(i)
                writeln('The pic download successed.\tNow sus:%5d,fail:%5d.'%(sus,fail))
            else:
                fail += 1
                failed_link.add(i)
                ffai.write(i + '\n')
                ffai.flush()
                writeln('The pic download failed.       \tNow sus:%5d,fail:%5d.'%(sus,fail))
        writeln( '.\n.\nAll Download Finisned.\nsus:%5d,fail:%5d.'%(sus,fail) )
    writeln('.\n.\nFin.\n')
    pass


