#!/usr/bin/env python
# encoding: utf-8
# Example: python zerochan.py 'Tales of Zestiria'
import os,re,sys,time
import requests
import lxml
from bs4 import BeautifulSoup
from os.path import join, getsize
import configparser


supported_site = ['konachan', 'zerochan', 'yandere']

'''
Return the download url and (optional: user login data)
'''
def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    url = config['DEFAULT']['url']
    data = dict((i,{}) for i in supported_site)
    for sec in config.sections():
        try:
            data[sec] = {'username':config[sec]['username'],'password':config[sec]['password']}
        except Exception as e:
            print(f'No login info found in {sec};')

    for sec in config.sections():
        try:
            data[sec]['url'] = config[sec]['url']
        except Exception as e:
            print(f'No url found in {sec};')
        
    print(f'url:{url}\ndata:{data}\n')
    return url,data






def main():
    read_config()
    pass

if __name__ == '__main__':
    main()