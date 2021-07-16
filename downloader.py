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
    login_data = {}
    for sec in config.sections():
        login_data[sec] = {'username':config[sec]['username'],'password':config[sec]['password']}
    print(f'url:{url}\nlogin_data:{login_data}\n')
    return url,login_data






def main():
    read_config()
    pass

if __name__ == '__main__':
    main()