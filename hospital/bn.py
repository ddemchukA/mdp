from django.shortcuts import render, redirect
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import numpy as np
import json
import requests
from bs4 import BeautifulSoup
import re
import smtplib
from datetime import datetime, date, time
from keras.models import load_model
from pandas import read_csv, DataFrame, Series
import pandas as pd
import numpy as np
import keras
import h5py# грузим пкет отвечающий за файлы hdf5
from .forms import insform, insformstudy,LoginForm,SearchForm, NP, NE, Dostav,SearchForm1,Priem
from .models import Insultik,patient,case, before, atributes, after, intime,intimetime,dostavlen,deadinroad
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
import pyAgrum as gum

class podg:
    param={}

    def __init__(self,nom):
        self.nom=nom

    def __get_case(self):
        ak=case.objects.get(pk=self.nom)
        return ak
#получение из БД
    def __get_bf(self):
        ak=before.objects.filter(case_id=self.nom)
        return ak
#Получение списка на вход сети кома Глазго
    def __get_glazgo(self,bf):
        sps=[]
        for kl in bf:
            if kl.atrib_id == 31:
                pv=kl.val_float
        self.param['glazg']=[0,0,0,0]
        if pv in range(0,7):
            self.param['glazg'][0]=1
        if pv in range(7,10):
            y=-1*0.5(pv-7)+1
            y1=0.5*(pv-9)+1
            self.param['glazg'][0]=round(y,1)
            self.param['glazg'][1]=round(y1,1)
        if pv > 9 and pv <10:
            self.param['glazg'][1]=1
        if pv in range(10,13):
            y=-1*0.5*(pv-10)+1
            y1=0.5*(pv-12)+1
            self.param['glazg'][1]=round(y,1)
            self.param['glazg'][2]=round(y1,1)
        if pv in range(12,15):
            y=-1*0.5*(pv-12)+1
            y1=0.5*(pv-14)+1
            self.param['glazg'][2]=round(y,1)
            self.param['glazg'][3]=round(y1,1)
        if pv > 14:
            self.param['glazg'][3]=1
#Список тип дыхания
    def __get_dix(self,bf):
        for kl in bf:
            if kl.atrib_id == 40:
                self.param['dix']=[1,0,0]
            if kl.atrib_id == 41:
                self.param['dix']=[0,1,0]
            if kl.atrib_id == 43 or kl.atrib_id == 44:
                self.param['dix']=[0,0,1]
#Список сатураций
    def __get_satur(self,bf):
        for kl in bf:
            if kl.atrib_id == 58:
                pv=kl.val_float
        self.param['satur']=[0,0,0]
        if pv < 89:
            self.param['satur'][0]=1
        if pv in range(89,92):
            y=-1*0.5*(pv-89)+1
            y1=0.5*(pv-91)+1
            self.param['satur'][0]=round(y,1)
            self.param['satur'][1]=round(y1,1)
        if pv > 91 and pv < 92:
            self.param['satur'][1]=1
        if pv in range(92,95):
            y=-1*0.5*(pv-92)+1
            y1=0.5*(pv-94)+1
            self.param['satur'][1]=round(y,1)
            self.param['satur'][2]=round(y1,1)
        if pv > 94:
            self.param['satur'][2]=1

#Список давление
    def __get_press(self,bf):
        for kl in bf:
            if kl.atrib_id == 68:
                pv=kl.val_text
        pk=pv.split("/")
        pk1=pk[0]
        pk2=int(pk1)
        self.param['press']=[0,0,0]
        if pk2 in range(0,95):
            self.param['press']=[1,0,0]
        if pk2 in range(95,106):
            y=-1*0.1*(pk2-95)+1
            y1=0.1*(pk2-95)
            self.param['press'][0]=round(y,1)
            self.param['press'][1]=round(y1,1)
        if pk2 in range(106,130):
            self.param['press']=[0,1,0]
        if pk2 in range(130,141):
            y=-1*0.1*(pk2-130)+1
            y1=0.1*(pk2-130)
            self.param['press'][1]=round(y,1)
            self.param['press'][2]=round(y1,1)
        if pk2 >= 141:
            self.param['press'][2]=1



#Список пульс
    def __get_puls(self,bf):
        for kl in bf:
            if kl.atrib_id == 67:
                pv=kl.val_float
        self.param['pulse']=[0,0,0]
        if pv in range(0,49):
            self.param['pulse'][0]=1
        if pv in range(50,61):
            y=-1*0.1*(pv-50)+1
            y1=0.1*(pv-60)+1
            self.param['pulse'][0]=round(y,1)
            self.param['pulse'][1]=round(y1,1)
        if pv in range(61,75):
            self.param['pulse'][1]=1
        if pv in range(75,86):
            y=-1*0.1*(pv-75)+1
            y1=0.1*(pv-85)+1
            self.param['pulse'][1]=round(y,1)
            self.param['pulse'][2]=round(y1,1)
        if pv > 85:
            self.param['pulse'][2]=1

#Список сатураций диурез
    def __get_diurez(self,bf):
        for kl in bf:
            if kl.atrib_id == 75:
                pv=kl.val_float
        self.param['diurez']=[0,0,0]
        if pv in range(0,20):
            self.param['diurez'][0]=1
        if pv in range(20,41):
            y=-1*0.05*(pv-20)+1
            y1=0.05*(pv-40)+1
            self.param['diurez'][0]=round(y,1)
            self.param['diurez'][1]=round(y1,1)
        if pv in range(41,90):
            self.param['diurez'][1]=1
        if pv in range(90,111):
            y=-1*0.05*(pv-90)+1
            y1=0.05*(pv-100)+1
            self.param['diurez'][1]=round(y,1)
            self.param['diurez'][2]=round(y1,1)
        if pv > 110:
            self.param['diurez'][2]=1

#Список тип транспорта
    def __get_transp(self,cs):
        if cs.id_trans_id == 1:
            self.param['transp']=[1,0]
        if cs.id_trans_id == 3:
            self.param['transp']=[0,1]
#Список комплексная оценка дороги
    def __get_road(self,cs):
        pv=cs.fromlpu.roadrate
        self.param['roadrate']=[0,0,0]
        if pv >=0 and pv < 1.8:
            self.param['roadrate'][0]=1
        if pv >= 1.8 and pv<=2.2:
            y=-1*2.5*round((pv-1.8),1)+1
            y1=2.5*round((pv-2.2),1)+1
            self.param['roadrate'][0]=round(y,1)
            self.param['roadrate'][1]=round(y1,1)
        if pv > 2.2 and pv < 2.8:
            self.param['roadrate'][1]=1
        if pv >= 2.8 and pv <= 3.2:
            y=-1*2.5*round((pv-2.8),1)+1
            y1=2.5*round((pv-3.2),1)+1
            self.param['roadrate'][1]=round(y,1)
            self.param['roadrate'][2]=round(y1,1)
        if pv > 3.2:
            self.param['roadrate'][2]=1


    def __formsp(self):
        cs=self.__get_case()
        bf=self.__get_bf()
        self.__get_glazgo(bf)
        self.__get_dix(bf)
        self.__get_satur(bf)
        self.__get_transp(cs)
        self.__get_road(cs)
        self.__get_press(bf)
        self.__get_puls(bf)
        self.__get_diurez(bf)
        return self.param

    def vivod(self):
        kk=self.__formsp()
        bn1=gum.BayesNet('MedRisk')
        riskdix = bn1.add(gum.LabelizedVariable ( 'riskdix' , 'itogdix', 2))
        bn1.cpt(riskdix).fillWith([0.0,0.0])
        riskdor = bn1.add(gum.LabelizedVariable ( 'riskdor' , 'itogdor', 2))
        bn1.cpt(riskdor).fillWith([0.0,0.0])
        riskheart = bn1.add(gum.LabelizedVariable ( 'riskheart' , 'itogheart', 2))
        bn1.cpt(riskheart).fillWith([0.0,0.0])
        obssom = bn1.add(gum.LabelizedVariable ( 'obssom' , 'itogobs', 2))
        bn1.cpt(obssom).fillWith([0.0,0.0])
        obsrisk = bn1.add(gum.LabelizedVariable ( 'obsrisk' , 'itogobsrisk', 2))
        bn1.cpt(obsrisk).fillWith([0.0,0.0])
        komgl=bn1.add('komgl',4)
        tipdix=bn1.add('tipdix',3)
        satur=bn1.add('satur',3)
        avto=bn1.add('avto',2)
        roadrate=bn1.add('roadrate',3)
        puls=bn1.add('puls',3)
        press=bn1.add('press',3)
        diurez=bn1.add('diurez',3)
        bn1=gum.fastBN("komgl[1,4]->riskdix[1,2];tipdix[1,3]->riskdix[1,2];satur[1,3]->riskdix[1,2];avto[1,2]->riskdor[1,2];roadrate[1,3]->riskdor[1,2];komgl[1,4]->riskdor[1,2];tipdix[1,3]->riskdor[1,2];diurez[1,3]->riskheart[1,2];press[1,3]->riskheart[1,2];puls[1,3]->riskheart[1,2];komgl[1,4]->obssom[1,2];tipdix[1,3]->obssom[1,2];satur[1,3]->obssom[1,2];press[1,3]->obssom[1,2];roadrate[1,3]->obssom[1,2];riskdix[1,2]->obsrisk[1,2];riskheart[1,2]->obsrisk[1,2];obssom[1,2]->obsrisk[1,2];riskdor[1,2]->obsrisk[1,2]")
        #Тут списки на вход сети
        #Например для комы глазго в интервале от 0-8 bn1.cpt("komgl")[:] =[1,0,0,0]
        bn1.cpt("komgl")[:] = kk['glazg']
        bn1.cpt("tipdix")[:] = kk['dix']
        bn1.cpt("satur")[:] = kk['satur']
        bn1.cpt("avto")[:] = kk['transp']
        bn1.cpt("roadrate")[:] = kk['roadrate']
        bn1.cpt("diurez")[:] = kk['diurez']
        bn1.cpt("puls")[:] = kk['pulse']
        bn1.cpt("press")[:] = kk['press']
        #Нарушения дыхания
        bn1.cpt("riskdix")[{'satur':0, 'tipdix':0, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("riskdix")[{'satur':0, 'tipdix':0, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("riskdix")[{'satur':0, 'tipdix':0, 'komgl':2}] = [0.9,0.1]
        bn1.cpt("riskdix")[{'satur':0, 'tipdix':0, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("riskdix")[{'satur':0, 'tipdix':1, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("riskdix")[{'satur':0, 'tipdix':1, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("riskdix")[{'satur':0, 'tipdix':1, 'komgl':2}] = [0.9,0.1]
        bn1.cpt("riskdix")[{'satur':0, 'tipdix':1, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("riskdix")[{'satur':0, 'tipdix':2, 'komgl':0}] = [0.6,0.4]
        bn1.cpt("riskdix")[{'satur':0, 'tipdix':2, 'komgl':1}] = [0.6,0.4]
        bn1.cpt("riskdix")[{'satur':0, 'tipdix':2, 'komgl':2}] = [0.5,0.5]
        bn1.cpt("riskdix")[{'satur':0, 'tipdix':2, 'komgl':3}] = [0.5,0.5]
        bn1.cpt("riskdix")[{'satur':1, 'tipdix':0, 'komgl':0}] = [0.7,0.3]
        bn1.cpt("riskdix")[{'satur':1, 'tipdix':0, 'komgl':1}] = [0.7,0.3]
        bn1.cpt("riskdix")[{'satur':1, 'tipdix':0, 'komgl':2}] = [0.7,0.3]
        bn1.cpt("riskdix")[{'satur':1, 'tipdix':0, 'komgl':3}] = [0.6,0.4]
        bn1.cpt("riskdix")[{'satur':1, 'tipdix':1, 'komgl':0}] = [0.7,0.3]
        bn1.cpt("riskdix")[{'satur':1, 'tipdix':1, 'komgl':1}] = [0.7,0.3]
        bn1.cpt("riskdix")[{'satur':1, 'tipdix':1, 'komgl':2}] = [0.7,0.3]
        bn1.cpt("riskdix")[{'satur':1, 'tipdix':1, 'komgl':3}] = [0.6,0.4]
        bn1.cpt("riskdix")[{'satur':1, 'tipdix':2, 'komgl':0}] = [0.5,0.5]
        bn1.cpt("riskdix")[{'satur':1, 'tipdix':2, 'komgl':1}] = [0.5,0.5]
        bn1.cpt("riskdix")[{'satur':1, 'tipdix':2, 'komgl':2}] = [0.5,0.5]
        bn1.cpt("riskdix")[{'satur':1, 'tipdix':2, 'komgl':3}] = [0.5,0.5]
        bn1.cpt("riskdix")[{'satur':2, 'tipdix':0, 'komgl':0}] = [0.6,0.4]
        bn1.cpt("riskdix")[{'satur':2, 'tipdix':0, 'komgl':1}] = [0.6,0.4]
        bn1.cpt("riskdix")[{'satur':2, 'tipdix':0, 'komgl':2}] = [0.5,0.5]
        bn1.cpt("riskdix")[{'satur':2, 'tipdix':0, 'komgl':3}] = [0.1,0.9]
        bn1.cpt("riskdix")[{'satur':2, 'tipdix':1, 'komgl':0}] = [0.7,0.3]
        bn1.cpt("riskdix")[{'satur':2, 'tipdix':1, 'komgl':1}] = [0.6,0.6]
        bn1.cpt("riskdix")[{'satur':2, 'tipdix':1, 'komgl':2}] = [0.3,0.7]
        bn1.cpt("riskdix")[{'satur':2, 'tipdix':1, 'komgl':3}] = [0.1,0.9]
        bn1.cpt("riskdix")[{'satur':2, 'tipdix':2, 'komgl':0}] = [0.3,0.7]
        bn1.cpt("riskdix")[{'satur':2, 'tipdix':2, 'komgl':1}] = [0.3,0.7]
        bn1.cpt("riskdix")[{'satur':2, 'tipdix':2, 'komgl':2}] = [0.3,0.7]
        bn1.cpt("riskdix")[{'satur':2, 'tipdix':2, 'komgl':3}] = [0.3,0.7]
        #Дорожные эксцессы
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':0, 'roadrate':0, 'avto':0}] = [0.6,0.4]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':0, 'roadrate':0, 'avto':1}] = [0.8,0.2]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':0, 'roadrate':1, 'avto':0}] = [0.5,0.5]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':0, 'roadrate':1, 'avto':1}] = [0.7,0.3]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':0, 'roadrate':2, 'avto':0}] = [0.5,0.5]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':0, 'roadrate':1, 'avto':1}] = [0.6,0.4]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':1, 'roadrate':0, 'avto':0}] = [0.3,0.7]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':1, 'roadrate':0, 'avto':1}] = [0.6,0.4]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':1, 'roadrate':1, 'avto':0}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':1, 'roadrate':1, 'avto':1}] = [0.5,0.5]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':1, 'roadrate':2, 'avto':0}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':1, 'roadrate':2, 'avto':1}] = [0.4,0.6]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':2, 'roadrate':0, 'avto':0}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':2, 'roadrate':0, 'avto':1}] = [0.4,0.6]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':2, 'roadrate':1, 'avto':0}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':2, 'roadrate':1, 'avto':1}] = [0.4,0.6]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':2, 'roadrate':2, 'avto':0}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':2, 'roadrate':2, 'avto':1}] = [0.3,0.7]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':3, 'roadrate':0, 'avto':0}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':3, 'roadrate':0, 'avto':1}] = [0.3,0.7]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':3, 'roadrate':1, 'avto':0}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':3, 'roadrate':1, 'avto':1}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':3, 'roadrate':2, 'avto':0}] = [0.02,0.98]
        bn1.cpt("riskdor")[{'tipdix':0, 'komgl':3, 'roadrate':2, 'avto':1}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':0, 'roadrate':0, 'avto':0}] = [0.4,0.6]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':0, 'roadrate':0, 'avto':1}] = [0.8,0.2]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':0, 'roadrate':1, 'avto':0}] = [0.3,0.7]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':0, 'roadrate':1, 'avto':1}] = [0.8,0.2]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':0, 'roadrate':2, 'avto':0}] = [0.3,0.7]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':0, 'roadrate':2, 'avto':1}] = [0.7,0.3]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':1, 'roadrate':0, 'avto':0}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':1, 'roadrate':0, 'avto':1}] = [0.4,0.6]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':1, 'roadrate':1, 'avto':0}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':1, 'roadrate':1, 'avto':1}] = [0.4,0.6]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':1, 'roadrate':2, 'avto':0}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':1, 'roadrate':2, 'avto':1}] = [0.3,0.7]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':2, 'roadrate':0, 'avto':0}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':2, 'roadrate':0, 'avto':1}] = [0.3,0.7]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':2, 'roadrate':1, 'avto':0}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':2, 'roadrate':1, 'avto':1}] = [0.3,0.7]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':2, 'roadrate':2, 'avto':0}] = [0.02,0.98]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':2, 'roadrate':2, 'avto':1}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':3, 'roadrate':0, 'avto':0}] = [0.02,0.98]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':3, 'roadrate':0, 'avto':1}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':3, 'roadrate':1, 'avto':0}] = [0.02,0.98]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':3, 'roadrate':1, 'avto':1}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':3, 'roadrate':2, 'avto':0}] = [0.02,0.98]
        bn1.cpt("riskdor")[{'tipdix':1, 'komgl':3, 'roadrate':2, 'avto':1}] = [0.02,0.98]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':0, 'roadrate':0, 'avto':0}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':0, 'roadrate':0, 'avto':1}] = [0.3,0.7]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':0, 'roadrate':1, 'avto':0}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':0, 'roadrate':1, 'avto':1}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':0, 'roadrate':2, 'avto':0}] = [0.02,0.98]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':0, 'roadrate':2, 'avto':1}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':1, 'roadrate':0, 'avto':0}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':1, 'roadrate':0, 'avto':1}] = [0.3,0.7]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':1, 'roadrate':1, 'avto':0}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':1, 'roadrate':1, 'avto':1}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':1, 'roadrate':2, 'avto':0}] = [0.02,0.98]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':1, 'roadrate':2, 'avto':1}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':2, 'roadrate':0, 'avto':0}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':2, 'roadrate':0, 'avto':1}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':2, 'roadrate':1, 'avto':0}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':2, 'roadrate':1, 'avto':1}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':2, 'roadrate':2, 'avto':0}] = [0.02,0.98]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':2, 'roadrate':2, 'avto':1}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':3, 'roadrate':0, 'avto':0}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':3, 'roadrate':0, 'avto':1}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':3, 'roadrate':1, 'avto':0}] = [0.1,0.9]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':3, 'roadrate':1, 'avto':1}] = [0.2,0.8]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':3, 'roadrate':2, 'avto':0}] = [0.02,0.98]
        bn1.cpt("riskdor")[{'tipdix':2, 'komgl':3, 'roadrate':2, 'avto':1}] = [0.1,0.9]
        #Риск ССС
        bn1.cpt("riskheart")[{'diurez':0, 'puls':0, 'press':0}] = [0.8,0.2]
        bn1.cpt("riskheart")[{'diurez':0, 'puls':0, 'press':1}] = [0.2,0.8]
        bn1.cpt("riskheart")[{'diurez':0, 'puls':0, 'press':2}] = [0.2,0.8]
        bn1.cpt("riskheart")[{'diurez':0, 'puls':1, 'press':0}] = [0.5,0.5]
        bn1.cpt("riskheart")[{'diurez':0, 'puls':1, 'press':1}] = [0.2,0.8]
        bn1.cpt("riskheart")[{'diurez':0, 'puls':1, 'press':2}] = [0.1,0.9]
        bn1.cpt("riskheart")[{'diurez':0, 'puls':2, 'press':0}] = [0.7,0.3]
        bn1.cpt("riskheart")[{'diurez':0, 'puls':2, 'press':1}] = [0.1,0.9]
        bn1.cpt("riskheart")[{'diurez':0, 'puls':2, 'press':2}] = [0.1,0.9]
        bn1.cpt("riskheart")[{'diurez':1, 'puls':0, 'press':0}] = [0.7,0.3]
        bn1.cpt("riskheart")[{'diurez':1, 'puls':0, 'press':1}] = [0.1,0.9]
        bn1.cpt("riskheart")[{'diurez':1, 'puls':0, 'press':2}] = [0.2,0.8]
        bn1.cpt("riskheart")[{'diurez':1, 'puls':1, 'press':0}] = [0.4,0.6]
        bn1.cpt("riskheart")[{'diurez':1, 'puls':1, 'press':1}] = [0.1,0.9]
        bn1.cpt("riskheart")[{'diurez':1, 'puls':1, 'press':2}] = [0.1,0.9]
        bn1.cpt("riskheart")[{'diurez':1, 'puls':2, 'press':0}] = [0.7,0.3]
        bn1.cpt("riskheart")[{'diurez':1, 'puls':2, 'press':1}] = [0.1,0.9]
        bn1.cpt("riskheart")[{'diurez':1, 'puls':2, 'press':2}] = [0.1,0.9]
        bn1.cpt("riskheart")[{'diurez':2, 'puls':0, 'press':0}] = [0.5,0.5]
        bn1.cpt("riskheart")[{'diurez':2, 'puls':0, 'press':1}] = [0.1,0.9]
        bn1.cpt("riskheart")[{'diurez':2, 'puls':0, 'press':2}] = [0.1,0.9]
        bn1.cpt("riskheart")[{'diurez':2, 'puls':1, 'press':0}] = [0.5,0.5]
        bn1.cpt("riskheart")[{'diurez':2, 'puls':1, 'press':1}] = [0.1,0.9]
        bn1.cpt("riskheart")[{'diurez':2, 'puls':1, 'press':2}] = [0.1,0.9]
        bn1.cpt("riskheart")[{'diurez':2, 'puls':2, 'press':0}] = [0.5,0.5]
        bn1.cpt("riskheart")[{'diurez':2, 'puls':2, 'press':1}] = [0.1,0.9]
        bn1.cpt("riskheart")[{'diurez':2, 'puls':2, 'press':2}] = [0.1,0.9]
        #Общесоматика
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':0, 'press':0, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':0, 'press':0, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':0, 'press':0, 'komgl':2}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':0, 'press':0, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':0, 'press':1, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':0, 'press':1, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':0, 'press':1, 'komgl':2}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':0, 'press':1, 'komgl':3}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':0, 'press':2, 'komgl':0}] = [0.98,0.02]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':0, 'press':2, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':0, 'press':2, 'komgl':2}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':0, 'press':2, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':1, 'press':0, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':1, 'press':0, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':1, 'press':0, 'komgl':2}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':1, 'press':0, 'komgl':3}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':1, 'press':1, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':1, 'press':1, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':1, 'press':1, 'komgl':2}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':1, 'press':1, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':1, 'press':2, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':1, 'press':2, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':1, 'press':2, 'komgl':2}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':1, 'press':2, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':2, 'press':0, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':2, 'press':0, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':2, 'press':0, 'komgl':2}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':2, 'press':0, 'komgl':2}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':2, 'press':1, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':2, 'press':1, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':2, 'press':1, 'komgl':2}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':2, 'press':1, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':2, 'press':2, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':2, 'press':2, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':2, 'press':2, 'komgl':2}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':0, 'roadrate':2, 'press':2, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':0, 'press':0, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':0, 'press':0, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':0, 'press':0, 'komgl':2}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':0, 'press':0, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':0, 'press':1, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':0, 'press':1, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':0, 'press':1, 'komgl':2}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':0, 'press':1, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':0, 'press':2, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':0, 'press':2, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':0, 'press':2, 'komgl':2}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':0, 'press':2, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':1, 'press':0, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':1, 'press':0, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':1, 'press':0, 'komgl':2}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':1, 'press':0, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':1, 'press':1, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':1, 'press':1, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':1, 'press':1, 'komgl':2}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':1, 'press':1, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':1, 'press':2, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':1, 'press':2, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':1, 'press':2, 'komgl':2}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':1, 'press':2, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':2, 'press':0, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':2, 'press':0, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':2, 'press':0, 'komgl':2}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':2, 'press':0, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':2, 'press':1, 'komgl':0}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':2, 'press':1, 'komgl':1}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':2, 'press':1, 'komgl':2}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':2, 'press':1, 'komgl':3}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':2, 'press':2, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':2, 'press':2, 'komgl':1}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':2, 'press':2, 'komgl':2}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':1, 'roadrate':2, 'press':2, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':0, 'press':0, 'komgl':0}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':0, 'press':0, 'komgl':1}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':0, 'press':0, 'komgl':2}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':0, 'press':0, 'komgl':3}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':0, 'press':1, 'komgl':0}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':0, 'press':1, 'komgl':1}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':0, 'press':1, 'komgl':2}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':0, 'press':1, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':0, 'press':2, 'komgl':0}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':0, 'press':2, 'komgl':1}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':0, 'press':2, 'komgl':2}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':0, 'press':2, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':1, 'press':0, 'komgl':0}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':1, 'press':0, 'komgl':1}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':1, 'press':0, 'komgl':2}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':1, 'press':0, 'komgl':3}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':1, 'press':1, 'komgl':0}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':1, 'press':1, 'komgl':1}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':1, 'press':1, 'komgl':2}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':1, 'press':1, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':1, 'press':2, 'komgl':0}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':1, 'press':2, 'komgl':1}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':1, 'press':2, 'komgl':2}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':1, 'press':2, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':2, 'press':0, 'komgl':0}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':2, 'press':0, 'komgl':1}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':2, 'press':0, 'komgl':2}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':2, 'press':0, 'komgl':3}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':2, 'press':1, 'komgl':0}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':2, 'press':1, 'komgl':1}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':2, 'press':1, 'komgl':2}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':2, 'press':1, 'komgl':3}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':2, 'press':2, 'komgl':0}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':2, 'press':2, 'komgl':1}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':2, 'press':2, 'komgl':2}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':0, 'tipdix':2, 'roadrate':2, 'press':2, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':0, 'press':0, 'komgl':0}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':0, 'press':0, 'komgl':1}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':0, 'press':0, 'komgl':2}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':0, 'press':0, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':0, 'press':1, 'komgl':0}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':0, 'press':1, 'komgl':1}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':0, 'press':1, 'komgl':2}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':0, 'press':1, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':0, 'press':2, 'komgl':0}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':0, 'press':2, 'komgl':1}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':0, 'press':2, 'komgl':2}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':0, 'press':2, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':1, 'press':0, 'komgl':0}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':1, 'press':0, 'komgl':1}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':1, 'press':0, 'komgl':2}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':1, 'press':0, 'komgl':3}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':1, 'press':1, 'komgl':0}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':1, 'press':1, 'komgl':1}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':1, 'press':1, 'komgl':2}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':1, 'press':1, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':1, 'press':2, 'komgl':0}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':1, 'press':2, 'komgl':1}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':1, 'press':2, 'komgl':2}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':1, 'press':2, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':2, 'press':0, 'komgl':0}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':2, 'press':0, 'komgl':1}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':2, 'press':0, 'komgl':2}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':2, 'press':0, 'komgl':3}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':2, 'press':1, 'komgl':0}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':2, 'press':1, 'komgl':1}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':2, 'press':1, 'komgl':2}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':2, 'press':1, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':2, 'press':2, 'komgl':0}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':2, 'press':2, 'komgl':1}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':2, 'press':2, 'komgl':2}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':0, 'roadrate':2, 'press':2, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':0, 'press':0, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':0, 'press':0, 'komgl':1}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':0, 'press':0, 'komgl':2}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':0, 'press':0, 'komgl':3}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':0, 'press':1, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':0, 'press':1, 'komgl':1}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':0, 'press':1, 'komgl':2}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':0, 'press':1, 'komgl':3}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':0, 'press':2, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':0, 'press':2, 'komgl':1}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':0, 'press':2, 'komgl':2}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':0, 'press':2, 'komgl':3}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':1, 'press':0, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':1, 'press':0, 'komgl':1}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':1, 'press':0, 'komgl':2}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':1, 'press':0, 'komgl':3}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':1, 'press':1, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':1, 'press':1, 'komgl':1}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':1, 'press':1, 'komgl':2}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':1, 'press':1, 'komgl':3}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':1, 'press':2, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':1, 'press':2, 'komgl':1}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':1, 'press':2, 'komgl':2}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':1, 'press':2, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':2, 'press':0, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':2, 'press':0, 'komgl':1}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':2, 'press':0, 'komgl':2}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':2, 'press':0, 'komgl':3}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':2, 'press':1, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':2, 'press':1, 'komgl':1}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':2, 'press':1, 'komgl':2}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':2, 'press':1, 'komgl':3}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':2, 'press':2, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':2, 'press':2, 'komgl':1}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':2, 'press':2, 'komgl':2}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':1, 'roadrate':2, 'press':2, 'komgl':3}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':0, 'press':0, 'komgl':0}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':0, 'press':0, 'komgl':1}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':0, 'press':0, 'komgl':2}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':0, 'press':0, 'komgl':3}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':0, 'press':1, 'komgl':0}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':0, 'press':1, 'komgl':1}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':0, 'press':1, 'komgl':2}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':0, 'press':1, 'komgl':3}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':0, 'press':2, 'komgl':0}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':0, 'press':2, 'komgl':1}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':0, 'press':2, 'komgl':2}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':0, 'press':2, 'komgl':3}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':1, 'press':0, 'komgl':0}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':1, 'press':0, 'komgl':1}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':1, 'press':0, 'komgl':2}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':1, 'press':0, 'komgl':3}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':1, 'press':1, 'komgl':0}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':1, 'press':1, 'komgl':1}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':1, 'press':1, 'komgl':2}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':1, 'press':1, 'komgl':3}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':1, 'press':2, 'komgl':0}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':1, 'press':2, 'komgl':1}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':1, 'press':2, 'komgl':2}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':1, 'press':2, 'komgl':3}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':2, 'press':0, 'komgl':0}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':2, 'press':0, 'komgl':1}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':2, 'press':0, 'komgl':2}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':2, 'press':0, 'komgl':3}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':2, 'press':1, 'komgl':0}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':2, 'press':1, 'komgl':1}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':2, 'press':1, 'komgl':2}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':2, 'press':1, 'komgl':3}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':2, 'press':2, 'komgl':0}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':2, 'press':2, 'komgl':1}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':2, 'press':2, 'komgl':2}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':1, 'tipdix':2, 'roadrate':2, 'press':2, 'komgl':3}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':0, 'press':0, 'komgl':0}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':0, 'press':0, 'komgl':1}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':0, 'press':0, 'komgl':2}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':0, 'press':0, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':0, 'press':1, 'komgl':0}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':0, 'press':1, 'komgl':1}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':0, 'press':1, 'komgl':2}] = [0.12,0.88]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':0, 'press':1, 'komgl':3}] = [0.02,0.98]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':0, 'press':2, 'komgl':0}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':0, 'press':2, 'komgl':1}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':0, 'press':2, 'komgl':2}] = [0.15,0.85]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':0, 'press':2, 'komgl':3}] = [0.02,0.98]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':1, 'press':0, 'komgl':0}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':1, 'press':0, 'komgl':1}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':1, 'press':0, 'komgl':2}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':1, 'press':0, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':1, 'press':1, 'komgl':0}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':1, 'press':1, 'komgl':1}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':1, 'press':1, 'komgl':2}] = [0.11,0.89]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':1, 'press':1, 'komgl':3}] = [0.01,0.99]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':1, 'press':2, 'komgl':0}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':1, 'press':2, 'komgl':1}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':1, 'press':2, 'komgl':2}] = [0.12,0.88]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':1, 'press':2, 'komgl':3}] = [0.02,0.98]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':2, 'press':0, 'komgl':0}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':2, 'press':0, 'komgl':1}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':2, 'press':0, 'komgl':2}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':2, 'press':0, 'komgl':3}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':2, 'press':1, 'komgl':0}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':2, 'press':1, 'komgl':1}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':2, 'press':1, 'komgl':2}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':2, 'press':1, 'komgl':3}] = [0.01,0.99]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':2, 'press':2, 'komgl':0}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':2, 'press':2, 'komgl':1}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':2, 'press':2, 'komgl':2}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':0, 'roadrate':2, 'press':2, 'komgl':3}] = [0.01,0.99]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':0, 'press':0, 'komgl':0}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':0, 'press':0, 'komgl':1}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':0, 'press':0, 'komgl':2}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':0, 'press':0, 'komgl':3}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':0, 'press':1, 'komgl':0}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':0, 'press':1, 'komgl':1}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':0, 'press':1, 'komgl':2}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':0, 'press':1, 'komgl':3}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':0, 'press':2, 'komgl':0}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':0, 'press':2, 'komgl':1}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':0, 'press':2, 'komgl':2}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':0, 'press':2, 'komgl':3}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':1, 'press':0, 'komgl':0}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':1, 'press':0, 'komgl':1}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':1, 'press':0, 'komgl':2}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':1, 'press':0, 'komgl':3}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':1, 'press':1, 'komgl':0}] = [0.9,0.1]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':1, 'press':1, 'komgl':1}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':1, 'press':1, 'komgl':2}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':1, 'press':1, 'komgl':3}] = [0.01,0.99]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':1, 'press':2, 'komgl':0}] = [0.8,0.2]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':1, 'press':2, 'komgl':1}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':1, 'press':2, 'komgl':2}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':1, 'press':2, 'komgl':3}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':2, 'press':0, 'komgl':0}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':2, 'press':0, 'komgl':1}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':2, 'press':0, 'komgl':2}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':2, 'press':0, 'komgl':3}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':2, 'press':1, 'komgl':0}] = [0.6,0.4]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':2, 'press':1, 'komgl':1}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':2, 'press':1, 'komgl':2}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':2, 'press':1, 'komgl':3}] = [0.01,0.99]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':2, 'press':2, 'komgl':0}] = [0.7,0.3]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':2, 'press':2, 'komgl':1}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':2, 'press':2, 'komgl':2}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':1, 'roadrate':2, 'press':2, 'komgl':3}] = [0.02,0.98]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':0, 'press':0, 'komgl':0}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':0, 'press':0, 'komgl':1}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':0, 'press':0, 'komgl':2}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':0, 'press':0, 'komgl':3}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':0, 'press':1, 'komgl':0}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':0, 'press':1, 'komgl':1}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':0, 'press':1, 'komgl':2}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':0, 'press':1, 'komgl':3}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':0, 'press':2, 'komgl':0}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':0, 'press':2, 'komgl':1}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':0, 'press':2, 'komgl':2}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':0, 'press':2, 'komgl':3}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':1, 'press':0, 'komgl':0}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':1, 'press':0, 'komgl':1}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':1, 'press':0, 'komgl':2}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':1, 'press':0, 'komgl':3}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':1, 'press':1, 'komgl':0}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':1, 'press':1, 'komgl':1}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':1, 'press':1, 'komgl':2}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':1, 'press':1, 'komgl':3}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':1, 'press':2, 'komgl':0}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':1, 'press':2, 'komgl':1}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':1, 'press':2, 'komgl':2}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':1, 'press':2, 'komgl':3}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':2, 'press':0, 'komgl':0}] = [0.5,0.5]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':2, 'press':0, 'komgl':1}] = [0.4,0.6]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':2, 'press':0, 'komgl':2}] = [0.3,0.7]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':2, 'press':0, 'komgl':3}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':2, 'press':1, 'komgl':0}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':2, 'press':1, 'komgl':1}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':2, 'press':1, 'komgl':2}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':2, 'press':1, 'komgl':3}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':2, 'press':2, 'komgl':0}] = [0.2,0.8]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':2, 'press':2, 'komgl':1}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':2, 'press':2, 'komgl':2}] = [0.1,0.9]
        bn1.cpt("obssom")[{'satur':2, 'tipdix':2, 'roadrate':2, 'press':2, 'komgl':3}] = [0.1,0.9]
        #Общий риск
        bn1.cpt("obsrisk")[{'obssom':0, 'riskheart':0, 'riskdix':0, 'riskdor':0}] = [0.98,0.02]
        bn1.cpt("obsrisk")[{'obssom':0, 'riskheart':0, 'riskdix':0, 'riskdor':1}] = [0.9,0.1]
        bn1.cpt("obsrisk")[{'obssom':0, 'riskheart':0, 'riskdix':1, 'riskdor':0}] = [0.9,0.1]
        bn1.cpt("obsrisk")[{'obssom':0, 'riskheart':0, 'riskdix':1, 'riskdor':1}] = [0.9,0.1]
        bn1.cpt("obsrisk")[{'obssom':0, 'riskheart':1, 'riskdix':0, 'riskdor':0}] = [0.9,0.1]
        bn1.cpt("obsrisk")[{'obssom':0, 'riskheart':1, 'riskdix':0, 'riskdor':1}] = [0.9,0.1]
        bn1.cpt("obsrisk")[{'obssom':0, 'riskheart':1, 'riskdix':1, 'riskdor':0}] = [0.8,0.2]
        bn1.cpt("obsrisk")[{'obssom':0, 'riskheart':1, 'riskdix':1, 'riskdor':1}] = [0.7,0.3]
        bn1.cpt("obsrisk")[{'obssom':1, 'riskheart':0, 'riskdix':0, 'riskdor':0}] = [0.9,0.1]
        bn1.cpt("obsrisk")[{'obssom':1, 'riskheart':0, 'riskdix':0, 'riskdor':1}] = [0.9,0.1]
        bn1.cpt("obsrisk")[{'obssom':1, 'riskheart':0, 'riskdix':1, 'riskdor':0}] = [0.9,0.1]
        bn1.cpt("obsrisk")[{'obssom':1, 'riskheart':0, 'riskdix':1, 'riskdor':1}] = [0.8,0.2]
        bn1.cpt("obsrisk")[{'obssom':1, 'riskheart':1, 'riskdix':0, 'riskdor':0}] = [0.7,0.3]
        bn1.cpt("obsrisk")[{'obssom':1, 'riskheart':1, 'riskdix':0, 'riskdor':1}] = [0.7,0.3]
        bn1.cpt("obsrisk")[{'obssom':1, 'riskheart':1, 'riskdix':1, 'riskdor':0}] = [0.3,0.7]
        bn1.cpt("obsrisk")[{'obssom':1, 'riskheart':1, 'riskdix':1, 'riskdor':1}] = [0.1,0.9]

        ie=gum.LazyPropagation(bn1)
        ie.makeInference()
        resu=ie.posterior('riskdix')
        resu1=ie.posterior('riskdor')
        resu2=ie.posterior('riskheart')
        resu3=ie.posterior('obssom')
        resu4=ie.posterior('obsrisk')
        k=resu.tolist()
        m=resu1.tolist()
        l=resu2.tolist()
        n=resu3.tolist()
        p=resu4.tolist()
        k1={}
        k1['riskdix']={}
        k1['riskdor']={}
        k1['riskheart']={}
        k1['obssom']={}
        k1['obsrisk']={}
        k1['riskdix']['critical']=round(k[0],3)
        k1['riskdix']['non_critical']=round(k[1],3)
        k1['riskdor']['Yes']=round(m[0],3)
        k1['riskdor']['No']=round(m[1],3)
        k1['riskheart']['Critical']=round(l[0],3)
        k1['riskheart']['NON_Critical']=round(l[1],3)
        k1['obssom']['Critical']=round(n[0],3)
        k1['obssom']['NON_Critical']=round(n[1],3)
        k1['obsrisk']['Risk']=round(p[0],3)
        k1['obsrisk']['NOT_Risk']=round(p[1],3)

        return k1
