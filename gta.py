#!/usr/bin/env python3 
'''
    Author : GYZheng, guanggyz@gmail.com
    Feature : A command line interface to do Eng<->Chines translation, utilize by Google Translation!
    Enviornment : Python3
    Update date : 2015.05.24
    Usage : gta -c "佛曰:不可說 不可說"
            gta -e "To do or not to do, that's the question"
'''
from html.parser import HTMLParser
import http.cookiejar, urllib.request,urllib.parse
import re
import sys

class GTAHTMLParser(HTMLParser):
    def _init(self,word):
        self.word = word
        self.wish_list =[]
        self.isStart = False
        self.isDone = False
    #override
    def handle_starttag(self,tag,attrs):
        if tag == 'span':
            for attr in attrs:
                if attr[0]=='id' and attr[1] =='result_box':                
                    self.isStart = True
        elif tag == 'div':
            for attr in attrs:
                if attr[0]=='id' and attr[1] =='gt-edit':
                    self.isDone = True
    def handle_data(self, data):
        #if not done and isTarget
        if self.isStart and not self.isDone:
            print (data)
        else:
            pass
    def handle_endtag(self,tag):
        pass
    def get_wish_list(self):
        return self.wish_list

class GTACrawer:
    def __init__(self,trans,word):
        #user input
        self.word = urllib.parse.quote(word)
        #default settings
        self.url_host = 'https://translate.google.com.tw'
        if trans == 'e2c':
            self.url_path = '/?sl=en&tl=zh-TW&q='+self.word
        elif trans == 'c2e':
            self.url_path = '/?sl=zh-TW&tl=en&q='+self.word
        self.wish_list= []
    def start(self):
        try:
            url = self.url_host+self.url_path
            request = urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"})
            response = urllib.request.urlopen(request)
            content = response.read().decode('utf-8','ignore')
            parser = GTAHTMLParser(strict=False)
            parser._init(self.word)
            parser.feed(content)
            '''
            if parser.get_wish_list():
                for item in parser.get_wish_list():
                    self.wish_list.append(item)
            '''
        except:
            print('exception')
    def get_result(self):
        return self.wish_list

if __name__ == '__main__':
    #word = input('word = ')
    isValidOpt = True
    if len(sys.argv) != 3:
        isValidOpt = False
        print('Usage: gta -type <word>')
        print('Example:')
        print('gta -e "An apple a day, keeps the doctor away"')
        print('gta -c "天天吃蘋果,醫生遠離我"')
    else:
        if sys.argv[1]=='-e':
            trans = 'e2c'
        elif sys.argv[1]=='-c':
            trans = 'c2e'
        else:
            isValidOpt = False
    if isValidOpt:
        word = sys.argv[2]
        gta = GTACrawer(trans,word)
        gta.start()
