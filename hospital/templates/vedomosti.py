import requests
from bs4 import BeautifulSoup
import re
import os
import hashlib
import json
from gtts import gTTS
import time

class vedomosti():
    rss=''
    spisok=[]
    hasm=''
    def __init__(self):
        self.rss= 'https://www.vedomosti.ru/rss/news'
        self.spisok = []
        self.hasm ='hash_ved.txt'

    def amici(sels,argi):
        a=[]
        r = requests.get(argi)
        soup = BeautifulSoup(r.content, 'html.parser')
        x=soup.find_all('div',{'class':'box-paragraph'},lambda y: y.name == 'p' and y.find_parent("p") is None)
        stroka=""
        for t in x:
            stroka=stroka+str(t.text)
        x1=soup.find_all('span',{'class':'tags__tag tags__tag--salmon'})
        stroka1=""
        for tagi in x1:
            stroka1=stroka1+tagi.find('a').text+','
        stroka=stroka.replace("\n"," ")
        stroka1=stroka1.replace("\n"," ")
        a.append(stroka)
        a.append(stroka1)
        return a

    def rssparse(self):
        with open(self.hasm, 'r') as f_in:
            hasm1 = json.load(f_in)
        f_in.close()
        r = requests.get(self.rss)
        soup = BeautifulSoup(r.content, 'lxml-xml')
        a=soup.find_all('item')
        for b in a:
            slv={}
            t=str(b.find('title').text)
            l=str(b.find('link').text)
            kar=''
            if b.find('enclosure'):
                kar=str(b.find('enclosure')['url'])
            h=str(hashlib.md5(t.encode("utf-8")).hexdigest())
            if h not in hasm1:
                hasm1.insert(0,h)
                with open(self.hasm, 'w') as f_out:
                    json.dump(hasm1, f_out)
                f_out.close()
                slv['title']=t
                slv['link']=l
                slv['img']=kar
                slv['has']=h
                km=self.amici(slv['link'])
                slv['text']=km[0]
                slv['tags']=km[1]
                self.spisok.append(slv)
        return self.spisok


    def printa(self):
        print( self.spisok,self.rss,self.hasm)
